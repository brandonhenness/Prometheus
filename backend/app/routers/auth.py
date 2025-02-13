# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user, get_user_permissions_from_ad
from fastapi import APIRouter, Depends, HTTPException, Request, status

router = APIRouter()


@router.get("/public")
async def public_route():
    return {"message": "This is a public route."}

@router.get("/admin")
async def admin_route(principal: str = Depends(get_current_user)):
    user_permissions = get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}

@router.get("/kerberos")
async def kerberos(request: Request):
    """
    Kerberos authentication endpoint.
    """
    auth_info = getattr(request.state, "auth_info", None)
    if not auth_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    # Use the 'upn' field as the user identifier (adjust as needed)
    user = auth_info.get("upn")
    # Save the user in the session
    request.state.session["user"] = user
    return {"message": f"Authenticated as {user}"}

@router.get("/protected")
async def protected_route(user: str = Depends(get_current_user)):
    """
    Protected route that requires a valid session.
    """
    return {"message": f"Hello, {user}!"}