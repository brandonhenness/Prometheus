# main.py
import logging
import redis.asyncio as redis

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from contextlib import asynccontextmanager

# Import middlewares
from app.middlewares.kerberos_auth import KerberosAuthMiddleware
from app.middlewares.redis_session import RedisSessionMiddleware

# Import routers
from app.routers.saml import router as saml_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.items import router as items_router

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create and attach a Redis client (with asyncio support) on startup
    app.state.redis = redis.Redis.from_url("redis://redis:6379", decode_responses=True)
    yield
    # Close the Redis client on shutdown
    await app.state.redis.close()

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
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(RedisSessionMiddleware, cookie_name="session", max_age=3600)
app.add_middleware(KerberosAuthMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.prometheus.osn.wa.gov", "canvas.prometheus.osn.wa.gov"])  # TODO: Move to config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prometheus.osn.wa.gov"],  # TODO: Move to config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
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
