# -*- coding: utf-8 -*-
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TodoItemRequest(BaseModel):
    name: str
    description: str


class TodoItem(TodoItemRequest):
    item_id: int


items: Dict[str, TodoItem] = {}


@app.get('/items')
def get_items() -> list[TodoItem]:
    return list(items.values())


@app.get('/items/{item_id}')
def get_items(item_id: str) -> TodoItem:
    return items[item_id]


@app.put('/items/{item_id}')
def update_item(item_id: str, item: TodoItemRequest) -> None:
    items[item_id] = TodoItem(
        item_id=item_id,
        name=item.name,
        description=item.description,
    )


@app.post('/items')
def create_item(item: TodoItemRequest):
    item_id = str(len(items) + 1)
    items[item_id] = TodoItem(
        item_id=item_id,
        name=item.name,
        description=item.description,
    )
