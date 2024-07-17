from typing import Union
from fastapi import FastAPI

app = FastAPI()


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
