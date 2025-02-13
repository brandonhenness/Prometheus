# routers/users.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/users/{username}")
async def read_user(username: str):
    return {"message": f"Hello {username}"}


@router.get("/user")
async def get_user(principal: str = Depends(get_current_user)):
    return {"username": principal}
