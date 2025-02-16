import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.utils.cookies import set_user_auth_cookie

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

router = APIRouter(prefix="/auth", tags=["auth"])

logging.basicConfig(level=logging.DEBUG)

@router.get("/public")
async def public_route():
    return {"message": "This is a public route."}

@router.get("/admin")
async def admin_route(principal: str = Depends(get_current_user)):
    # For example purposes; replace with your real permission-check logic.
    user_permissions = ["admin"]  # Replace with: get_user_permissions_from_ad(principal)
    if "admin" not in user_permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "This is an admin route."}

@router.get("/login")
async def login(
    request: Request, 
    response: Response, 
    user: dict = Depends(get_current_user)
):
    return_to = request.query_params.get("returnTo", "/")
    absolute_url = f"{FRONTEND_URL}{return_to}"
    logging.debug(f"User {user['upn']} authenticated. Redirecting to {absolute_url}")
    
    return RedirectResponse(url=absolute_url)

@router.get("/protected")
async def protected_route(user: str = Depends(get_current_user)):
    """
    Protected route that requires a valid session.
    """
    return {"message": f"Hello, {user}!"}

# Optionally define a User model
class User(BaseModel):
    username: str
    upn: str = None
    email: str = None
    first_name: str = None
    last_name: str = None

@router.get("/session", response_model=User)
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Returns information about the currently authenticated user.
    """
    return User(**user)
