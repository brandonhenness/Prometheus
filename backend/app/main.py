from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
import kerberos

security = HTTPBearer()
app = FastAPI()

class KerberosAuthMiddleware:
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                result = kerberos.authGSSServerInit("HTTP@your.domain.com")
                kerberos.authGSSServerStep(result, auth_header.split()[1])
                principal = kerberos.authGSSServerUserName(result)
                request.state.principal = principal
                kerberos.authGSSServerClean(result)
            except kerberos.GSSError as e:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Kerberos authentication failed"},
                    headers={"WWW-Authenticate": "Negotiate"},
                )
        else:
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

# Your existing routes with modified dependencies
@app.get("/login")
async def login(principal: str = Depends(requires_auth)):
    return JSONResponse(content={"message": f"Authenticated as {principal}"})

@app.get("/user")
async def get_user(principal: str = Depends(requires_auth)):
    return JSONResponse(content={"username": principal})

@app.get("/protected")
async def protected_route(principal: str = Depends(requires_auth)):
    return JSONResponse(content={"message": f"Authenticated as {principal}"})


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/hello")
async def hello():
    return {"message": "Hello API"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/public")
async def public_route():
    return JSONResponse(content={"message": "This is a public route."})


@app.get("/admin", dependencies=[Depends(requires_auth)])
async def admin_route(
    request: Request,
    permissions: None = Depends(lambda request: check_permissions(request, "admin")),
):
    return JSONResponse(content={"message": "This is an admin route."})


# Example function to check user's permissions
def check_permissions(request: Request, required_permission: str):
    user_info = request.state.principal

    # Here, you would query your AD or a permissions database to check the user's permissions
    # For simplicity, we'll assume user_info contains a list of permissions
    user_permissions = get_user_permissions_from_ad(user_info)

    if required_permission not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


def get_user_permissions_from_ad(user_info):
    # This is a placeholder function. Replace with actual AD query logic.
    # For example, using LDAP3 to query user's groups and translate them to permissions.
    if user_info == "allowed_user":
        return ["read", "write", "admin"]
    else:
        return ["read"]
