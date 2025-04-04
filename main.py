from fastapi import FastAPI,Query
from pydantic import BaseModel
from typing import Annotated

import uvicorn
app = FastAPI()
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool|None = None
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Annotated[str|None,Query(min_length=10)] = None)->Item:
    item = Item(name="Item Name", price=100.0, is_offer=True)
    if q:
        item.name += f" - {q}"
    return item
@app.get("/items/")
async def read_items(q: Annotated[str|None,Query(max_length=10)] = None)->Item:
    item = Item(name="Item Name", price=100.0, is_offer=True)
    if q:
        item.name += f" - {q}"
    return item
@app.post("/items/")
async def create_items(item:Item)->Item:
    return item
if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0",port=8000, app=app, reload=True)
# To run the server, use the command: uvicorn main:app --reload
