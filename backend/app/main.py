# main.py
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.middlewares.kerberos_auth import KerberosAuthMiddleware

from app.routers.saml import router as saml_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.items import router as items_router

from saml2.server import Server as Saml2IdPServer
from saml2.config import IdPConfig
from app.saml_idp_config import IDP_CONFIG

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

idp_config = IdPConfig()
idp_config.load(IDP_CONFIG)
saml_idp = Saml2IdPServer(config=idp_config)

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
        {
            "name": "saml",
            "description": "Operations related to SAML2 Identity Provider",
        },
    ],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(KerberosAuthMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.prometheus.osn.wa.gov", "canvas.prometheus.osn.wa.gov"]) #TODO: Move to config

app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, tags=["users"])
app.include_router(items_router, tags=["items"])
app.include_router(saml_router, prefix="/saml", tags=["saml"])


@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")


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


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "Not Found"},
    )
