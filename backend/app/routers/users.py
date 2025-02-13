# routers/users.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from pydantic import BaseModel

# Optionally define a User model
class User(BaseModel):
    username: str
    upn: str = None
    email: str = None
    first_name: str = None
    last_name: str = None

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """
    Returns information about the currently authenticated user.
    """
    # Assuming get_current_user returns something like {"username": "example"}
    return User(**user)


@router.get("/{user_id}")
async def get_user_by_id(user_id: str):
    # Logic to retrieve user by id
    pass


@router.put("/{user_id}")
async def update_user(user_id: str, user_data: User):
    # Logic to update user data
    pass
