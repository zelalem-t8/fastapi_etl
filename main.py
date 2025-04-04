from fastapi import FastAPI,Query,Path
from pydantic import BaseModel,Field
from typing import Annotated,Literal

import uvicorn
app = FastAPI()
class Image(BaseModel):
    url:str
    name:str|None = None
    model_config={
        "json_schema_extra":{
            "examples":[{
                "url":"https://example.com/image.png",
                "name":"example"
            }]
        }
    }
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool|None = None
    images: list[Image]|None = None
    model_config={
        "json_schema_extra":{
            "examples":[{
                "name":"cosmetic",
                "price":100.0,
                "is_offer":True
            }]
        }
    }
class FilterParams(BaseModel):
    limit:int=Field(100,ge=0,le=1000)
    offset:int=Field(0,ge=0,le=1000)
    tags:list[str]|None = []
    order_by: Literal["created_at", "updated_at"] = "created_at"
    model_config={
        "json_schema_extra": {
            "example":{
                "limit": 100,
                "offset": 0,
                "tags": ["tag1", "tag2"],
                "order_by": "created_at"
            }
        }

    }

    
@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[int,Path(title="The item id to be retrived")], q: Annotated[FilterParams,Query()] = None)->Item:
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
