from typing import Union
from fastapi import FastAPI
from app.five_nine_one.helpers.get_content import get_content

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/rent/five_nine_one/content")
def get_five_nine_one_content():
    return get_content()