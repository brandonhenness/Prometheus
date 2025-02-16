# routers/items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
