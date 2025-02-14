# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user, get_user_permissions_from_ad

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/public")
async def public_route():
    return {"message": "This is a public route."}


@router.get("/admin")
async def admin_route(principal: str = Depends(get_current_user)):
    user_permissions = get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}


@router.get("/login")
async def login(request: Request, response: Response, user: dict = Depends(get_current_user)):
    """
    Kerberos authentication endpoint.
    The dependency handles authentication and sets the cookie.
    """
    return JSONResponse({"message": f"Authenticated as {user['upn']}"})


@router.get("/protected")
async def protected_route(user: str = Depends(get_current_user)):
    """
    Protected route that requires a valid session.
    """
    return {"message": f"Hello, {user}!"}