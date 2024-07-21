from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi_kerberos import KerberosMiddleware, requires_auth
from starlette.responses import JSONResponse

app = FastAPI()

app.add_middleware(KerberosMiddleware)


@app.get("/login", dependencies=[Depends(requires_auth)])
async def login(request: Request):
    # Extract user info from the request
    user_info = request.state.principal
    return JSONResponse(content={"message": f"Authenticated as {user_info}"})


@app.get("/user", dependencies=[Depends(requires_auth)])
async def get_user(request: Request):
    user_info = request.state.principal
    # You can also query AD for additional user information if needed
    return JSONResponse(content={"username": user_info})


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


@app.get("/protected", dependencies=[Depends(requires_auth)])
async def protected_route(request: Request):
    return JSONResponse(
        content={"message": f"Authenticated as {request.state.principal}"}
    )


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
