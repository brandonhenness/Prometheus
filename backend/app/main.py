import logging
import traceback
import base64
import os
import gssapi
import ldap3

from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware


# Set up logging to display debug output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title="Prometheus API",
    description="API for Prometheus web application",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operations related to authentication",
        },
        {
            "name": "users",
            "description": "Operations related to users",
        },
        {
            "name": "items",
            "description": "Operations related to items",
        },
    ],

)

app.mount("/static", StaticFiles(directory="static"), name="static")

class KerberosAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug("Starting Kerberos authentication middleware dispatch.")
        request.state.principal = None

        auth_header = request.headers.get("Authorization")
        logger.debug(f"Authorization header: {auth_header}")
        if auth_header and auth_header.startswith("Negotiate "):
            spnego_token = auth_header[len("Negotiate "):].strip()
            logger.debug(f"Extracted SPNEGO token: {spnego_token}")

            try:
                service_principal = f'{os.getenv("KRB_SERVICE")}/{os.getenv("KRB_HOST")}@{os.getenv("KRB_REALM")}'
                logger.debug(f"Using service principal: {service_principal}")

                # Create server credentials (usage="accept")
                server_creds = gssapi.Credentials(usage="accept")
                # Create a security context for accepting the token
                sec_context = gssapi.SecurityContext(creds=server_creds, usage="accept")

                # Decode the incoming SPNEGO token (Base64)
                in_token = base64.b64decode(spnego_token)
                logger.debug("Calling SecurityContext.step() with the incoming token.")
                out_token = sec_context.step(in_token)
                logger.debug(f"SecurityContext.step() returned: {out_token}")

                if sec_context.complete:
                    principal = str(sec_context.initiator_name)
                    request.state.principal = principal
                    logger.info(f"Authentication complete. Principal: {principal}")
                else:
                    out_token_b64 = base64.b64encode(out_token).decode('ascii') if out_token else ""
                    logger.warning("Authentication incomplete; additional token exchange required.")
                    return Response(
                        status_code=401,
                        headers={"WWW-Authenticate": f"Negotiate {out_token_b64}"}
                    )
            except Exception as e:
                logger.error(f"Kerberos error: {e}")
                logger.debug(traceback.format_exc())
        else:
            logger.debug("No valid Negotiate Authorization header found.")

        response = await call_next(request)
        logger.debug("Exiting Kerberos authentication middleware dispatch.")
        return response

app.add_middleware(KerberosAuthMiddleware)

def requires_auth(request: Request):
    logger.debug("Checking if request is authenticated.")
    if not request.state.principal:
        logger.warning("Authentication required but principal is missing.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Negotiate"},
        )
    logger.debug(f"Request authenticated as: {request.state.principal}")
    return request.state.principal

def get_user_permissions_from_ad(user_info: str):
    LDAP_SERVER = os.getenv("LDAP_SERVER")
    LDAP_USER = os.getenv("LDAP_USER")
    LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
    LDAP_DOMAIN = os.getenv("LDAP_DOMAIN")

    user_permissions = ["read"]

    user_account = user_info.split("@")[0]

    try:
        server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, LDAP_USER, LDAP_PASSWORD, auto_bind=True)
    except Exception as e:
        print(f"LDAP connection error: {e}")
        return user_permissions

    search_filter = f"(|(sAMAccountName={user_account})(userPrincipalName={user_info}))"
    try:
        conn.search(
            search_base=LDAP_DOMAIN,
            search_filter=search_filter,
            attributes=["memberOf"],
        )
    except Exception as e:
        print(f"LDAP search error: {e}")
        return user_permissions

    if not conn.entries:
        return user_permissions

    user_entry = conn.entries[0]
    group_dns = user_entry.memberOf.values if "memberOf" in user_entry else []

    for group_dn in group_dns:
        if "MyAppAdmins" in group_dn:
            user_permissions.append("admin")

    return user_permissions


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Visit /docs for API documentation"}


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_css_url="/static/swagger-ui.css",
        swagger_ui_parameters={"syntaxHighlight.theme": "monokai"},
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title,
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/auth", tags=["auth"])
async def auth(principal: str = Depends(requires_auth)):
    """Return a simple message for authenticated users."""
    logger.debug(f"Returning auth response for principal: {principal}")
    return {"message": f"Hello, {principal}!"}


@app.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"message": f"Hello {username}"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/public", tags=["auth"])
async def public_route():
    return {"message": "This is a public route."}


@app.get("/login", tags=["auth"])
async def login(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}


@app.get("/user", tags=["users"])
async def get_user(principal: str = Depends(requires_auth)):
    return {"username": principal}


@app.get("/protected", tags=["auth"])
async def protected_route(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}


@app.get("/admin", tags=["auth"])
async def admin_route(principal: str = Depends(requires_auth)):
    user_permissions = get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "Not Found"},
    )