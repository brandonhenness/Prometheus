# routers/saml.py
import logging

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from saml2.config import IdPConfig
from saml2.server import Server as Saml2IdPServer
from saml2.metadata import entity_descriptor
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST

from app.saml_idp_config import IDP_CONFIG  # Your custom config dict

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
    The SP sends an AuthnRequest here (via GET or POST).
    We'll parse and validate it, authenticate the user (via Kerberos if needed),
    then return a signed SAMLResponse with the user's identity.
    """

    # 1) Collect SAMLRequest & RelayState depending on GET or POST
    saml_request = None
    relay_state = None

    if request.method == "POST":
        # Ensure you have pip install python-multipart
        form_data = await request.form()
        saml_request = form_data.get("SAMLRequest")
        relay_state = form_data.get("RelayState")
    else:  # GET
        query_params = dict(request.query_params)
        saml_request = query_params.get("SAMLRequest")
        relay_state = query_params.get("RelayState")

    if not saml_request:
        logger.error("No SAMLRequest found in /sso request.")
        return HTMLResponse("No SAMLRequest provided.", status_code=400)

    # 2) Parse the AuthnRequest
    try:
        req_info = saml_idp.parse_authn_request(saml_request, BINDING_HTTP_REDIRECT)
    except Exception:
        logger.exception("Error parsing AuthnRequest")
        return HTMLResponse("Invalid or malformed SAMLRequest.", status_code=400)

    if not req_info:
        return HTMLResponse("Unable to parse SAMLRequest.", status_code=400)

    # 3) Check if user is authenticated (Kerberos)
    user_id = getattr(request.state, "principal", None)
    if not user_id:
        # Trigger Kerberos if missing
        logger.warning("User not authenticated for SSO. Sending Kerberos challenge.")
        return Response(
            status_code=401,
            headers={"WWW-Authenticate": "Negotiate"},
            content="Please authenticate with Kerberos"
        )

    # 4) Build a SAML AuthnResponse (user is authenticated now)
    try:
        resp_args = saml_idp.response_args(req_info.message)  # decipher the SP, ACS URL, etc.
        identity = {
            "uid": [user_id],
            "username": [user_id],
            # Add more SAML attributes if needed
        }
        authn_resp = saml_idp.create_authn_response(
            identity=identity,
            userid=user_id,
            authn={"class_ref": "urn:oasis:names:tc:SAML:2.0:ac:classes:Kerberos"},  # or Password, etc.
            **resp_args
        )

        # 5) Apply the correct binding (Redirect or POST) to send response
        binding, destination = resp_args["binding"], resp_args["destination"]
        http_args = saml_idp.apply_binding(
            binding,
            str(authn_resp),
            destination,
            relay_state,
            response=True
        )

        # 6) Return the correct response type
        if binding == BINDING_HTTP_REDIRECT:
            # Typically the Location header is in http_args["headers"]
            for (k, v) in http_args["headers"]:
                if k.lower() == "location":
                    return RedirectResponse(url=v)
            return HTMLResponse("No redirect URL found.", status_code=500)

        elif binding == BINDING_HTTP_POST:
            # Usually "data" is an auto-submitting HTML form
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
    return HTMLResponse("SLO endpoint not implemented.", status_code=501)
