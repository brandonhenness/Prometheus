import os
from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException, status
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Set root path based on environment
root_path = "/api" if os.getenv("DEVELOPMENT_MODE", "False").lower() == "true" else ""
app = FastAPI(root_path=root_path)

class KerberosAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Temporary mock authentication for development
        if os.getenv("DEVELOPMENT_MODE", "False").lower() == "true":
            request.state.principal = "devuser@EXAMPLE.COM"
        else:
            # Real Kerberos implementation would go here
            request.state.principal = None
        
        response = await call_next(request)
        return response

app.add_middleware(KerberosAuthMiddleware)

def requires_auth(request: Request):
    if not request.state.principal:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Negotiate"},
        )
    return request.state.principal

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = app.openapi()
    
    # Add server configurations
    servers = []
    if os.getenv("DEVELOPMENT_MODE", "False").lower() == "true":
        servers.append({"url": "/api", "description": "Development environment"})
    else:
        servers.append({"url": "/", "description": "Production environment"})
    
    openapi_schema["servers"] = servers
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Public endpoints
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/public")
async def public_route():
    return {"message": "This is a public route."}

# Authenticated endpoints
@app.get("/login")
async def login(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}

@app.get("/user")
async def get_user(principal: str = Depends(requires_auth)):
    return {"username": principal}

@app.get("/protected")
async def protected_route(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}

# Admin endpoints
@app.get("/admin")
async def admin_route(principal: str = Depends(requires_auth)):
    user_permissions = get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}

# Example endpoints
@app.get("/")
async def root():
    return {"message": "Visit /docs for API documentation"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Helper functions
def get_user_permissions_from_ad(user_info):
    return ["read", "write", "admin"] if user_info == "devuser@EXAMPLE.COM" else ["read"]

# Error handler for documentation
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    if request.url.path in ["/docs", "/redoc"]:
        return JSONResponse(
            status_code=307,
            headers={"Location": f"{root_path}/docs" if root_path else "/docs"}
        )
    return JSONResponse(
        status_code=404,
        content={"message": "Not found"}
    )