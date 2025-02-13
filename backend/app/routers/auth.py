# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import requires_auth, get_user_permissions_from_ad

router = APIRouter()

@router.get("/auth")
async def auth_route(principal: str = Depends(requires_auth)):
    """
    Return a simple message for authenticated users.
    """
    return {"message": f"Hello, {principal}!"}


@router.get("/public")
async def public_route():
    return {"message": "This is a public route."}


@router.get("/login")
async def login(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}


@router.get("/protected")
async def protected_route(principal: str = Depends(requires_auth)):
    return {"message": f"Authenticated as {principal}"}


@router.get("/admin")
async def admin_route(principal: str = Depends(requires_auth)):
    user_permissions = get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}
