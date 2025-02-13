# routers/users.py
from fastapi import APIRouter, Depends
from app.dependencies import requires_auth

router = APIRouter()

@router.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}


@router.get("/user")
async def get_user(principal: str = Depends(requires_auth)):
    return {"username": principal}
