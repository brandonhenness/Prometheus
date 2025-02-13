# routers/saml.py
import logging

from fastapi import APIRouter, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from saml2.config import IdPConfig
from saml2.server import Server as Saml2IdPServer
from saml2.metadata import entity_descriptor
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NameID

from app.saml_idp_config import IDP_CONFIG

logger = logging.getLogger(__name__)

router = APIRouter()

# 1) Build the IdP server at import time (or consider doing it on startup)
idp_config = IdPConfig()
idp_config.load(IDP_CONFIG)
saml_idp = Saml2IdPServer(config=idp_config)


@router.get("/metadata", include_in_schema=False)
async def idp_metadata():
    """
    (Optional) Endpoint to serve IdP metadata, so SPs can integrate.
    You typically need to sign this metadata for production usage.
    """
    metadata_str = str(entity_descriptor(idp_config))

    return HTMLResponse(content=metadata_str, status_code=200, media_type="text/xml")


@router.get("/sso")
@router.post("/sso")
async def single_sign_on_service(request: Request):
    """
    IdP SingleSignOnService endpoint.
    Parses the AuthnRequest, ensures the user is authenticated via Kerberos,
    and then returns a signed SAMLResponse.
    """
    # Extract SAML parameters
    if request.method == "POST":
        form_data = await request.form()
        saml_request = form_data.get("SAMLRequest")
        relay_state = form_data.get("RelayState")
        sigalg = None
        signature = None
    else:
        query_params = dict(request.query_params)
        saml_request = query_params.get("SAMLRequest")
        relay_state = query_params.get("RelayState")
        sigalg = query_params.get("SigAlg")
        signature = query_params.get("Signature")

    if not saml_request:
        logger.error("No SAMLRequest found in /sso request.")
        return HTMLResponse("No SAMLRequest provided.", status_code=400)

    try:
        req_info = saml_idp.parse_authn_request(
            saml_request,
            BINDING_HTTP_REDIRECT,
            relay_state=relay_state,
            sigalg=sigalg,
            signature=signature
        )
    except Exception as e:
        logger.exception(f"Error parsing AuthnRequest: {e}")
        return HTMLResponse("Invalid or malformed SAMLRequest.", status_code=400)

    if not req_info:
        return HTMLResponse("Unable to parse SAMLRequest.", status_code=400)

    # Instead of checking request.state.principal, retrieve the full auth_info dictionary
    auth_info = getattr(request.state, "auth_info", None)
    if not auth_info or "upn" not in auth_info:
        logger.warning("User not authenticated for SSO. Sending Kerberos challenge.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Negotiate"},
        )

    # Use the Windows Domain Qualified Name from the auth_info
    user_id = auth_info["upn"]
    logger.debug(f"Using UPN for SAML response: {user_id}")

    # Build the identity dictionary (you can include additional attributes if needed)
    identity = {
        "uid": [user_id],
        "username": [user_id],
    }

    # Create a NameID object in the WindowsDomainQualifiedName format
    raw_nameid = NameID(
        text=user_id,
        format="urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName",
        name_qualifier=IDP_CONFIG["entityid"],
        sp_name_qualifier="http://canvas.prometheus.osn.wa.gov/saml2", #TODO: Move this to a config
    )

    try:
        # Obtain response parameters (such as the destination URL)
        resp_args = saml_idp.response_args(req_info.message)
        # Create the SAML AuthnResponse, passing our custom NameID via the 'name_id' parameter
        authn_resp = saml_idp.create_authn_response(
            identity=identity,
            userid=user_id,
            name_id=raw_nameid,
            authn={"class_ref": "urn:oasis:names:tc:SAML:2.0:ac:classes:Kerberos"},
            **resp_args
        )

        # Apply the binding (Redirect or POST) to produce the proper HTTP response
        binding, destination = resp_args["binding"], resp_args["destination"]
        http_args = saml_idp.apply_binding(
            binding,
            str(authn_resp),
            destination,
            relay_state,
            response=True
        )

        if binding == BINDING_HTTP_REDIRECT:
            for (k, v) in http_args["headers"]:
                if k.lower() == "location":
                    return RedirectResponse(url=v)
            return HTMLResponse("No redirect URL found.", status_code=500)
        elif binding == BINDING_HTTP_POST:
            return HTMLResponse(content=http_args["data"], status_code=200)
        else:
            return HTMLResponse("Unsupported binding.", status_code=400)
    except Exception:
        logger.exception("Error creating or applying binding for AuthnResponse")
        return HTMLResponse("Internal SAML processing error.", status_code=500)


@router.get("/slo")
@router.post("/slo")
async def single_logout_service(request: Request):
    """
    (Optional) IdP SingleLogoutService endpoint.
    The SP might send a LogoutRequest here to end the user's session.
    """
    return HTMLResponse("SLO endpoint not implemented.", status_code=501) #TODO: Implement this
