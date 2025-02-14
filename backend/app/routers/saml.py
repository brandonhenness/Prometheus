# routers/saml.py
import logging

from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from saml2.config import IdPConfig
from saml2.server import Server as Saml2IdPServer
from saml2.metadata import entity_descriptor
from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NameID

from app.saml_idp_config import IDP_CONFIG
from app.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# We'll use these globals for lazy initialization.
_saml_idp = None
_idp_config = None

def get_saml_server() -> Saml2IdPServer:
    """
    Lazy-load the SAML IdP server.
    If there's a problem loading the configuration or creating the server,
    log the error and return None.
    """
    global _saml_idp, _idp_config
    if _saml_idp is None:
        try:
            _idp_config = IdPConfig()
            _idp_config.load(IDP_CONFIG)
            _saml_idp = Saml2IdPServer(config=_idp_config)
        except Exception as e:
            logger.exception("Error initializing SAML IdP server. SAML functionality will be disabled.")
            # Mark as disabled by setting to None (or you could set a flag)
            _saml_idp = None
    return _saml_idp

@router.get("/metadata", include_in_schema=False)
async def idp_metadata():
    """
    Endpoint to serve IdP metadata. If the SAML server is not available,
    returns a 503 response.
    """
    saml_idp = get_saml_server()
    if saml_idp is None or _idp_config is None:
        return HTMLResponse("SAML functionality currently unavailable.", status_code=503)
    metadata_str = str(entity_descriptor(_idp_config))
    return HTMLResponse(content=metadata_str, status_code=200, media_type="text/xml")

@router.get("/sso")
@router.post("/sso")
async def single_sign_on_service(
    request: Request, current_user: dict = Depends(get_current_user)
):
    """
    IdP SingleSignOnService endpoint.
    If the SAML server isn't available, returns a 503.
    """
    saml_idp = get_saml_server()
    if saml_idp is None:
        return HTMLResponse("SAML functionality currently unavailable.", status_code=503)

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

    user_id = current_user.get("upn")
    logger.debug(f"Using UPN for SAML response: {user_id}")

    identity = {
        "uid": [user_id],
        "username": [current_user.get("username")],
        "email": [current_user.get("email")],
        "first_name": [current_user.get("first_name")],
        "last_name": [current_user.get("last_name")],
    }

    raw_nameid = NameID(
        text=user_id,
        format="urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName",
        name_qualifier=IDP_CONFIG["entityid"],
        sp_name_qualifier="http://canvas.prometheus.osn.wa.gov/saml2",  # TODO: Move this to a config
    )

    try:
        resp_args = saml_idp.response_args(req_info.message)
        authn_resp = saml_idp.create_authn_response(
            identity=identity,
            userid=user_id,
            name_id=raw_nameid,
            authn={"class_ref": "urn:oasis:names:tc:SAML:2.0:ac:classes:Kerberos"},
            **resp_args
        )

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
    IdP SingleLogoutService endpoint.
    """
    return HTMLResponse("SLO endpoint not implemented.", status_code=501)  # TODO: Implement this
