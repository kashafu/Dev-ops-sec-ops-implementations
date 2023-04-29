# -*- coding: utf-8 -*-
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel
import json
import redis

app = FastAPI()

r = redis.Redis(host='redis', port=6379, decode_responses=True)


class TaskRequest(BaseModel):
    name: str
    description: str


class Task(TaskRequest):
    item_id: int


tasks: Dict[str, Task] = {}


@app.get('/tasks')
def get_tasks() -> List[Task]:
    keys = r.keys()

    tasks = []
    for key in keys:
        print(key)
        value = json.loads(r.get(key))
        tasks.append(Task(
            item_id=key,
            name= value['name'],
            description = value['description'],
        ))
    return tasks


@app.get('/tasks/{item_id}')
def get_task(item_id: str) -> Task:
    value = json.loads(r.get(f'tasks:{item_id}'))
    return Task(
        item_id= item_id,
        name= value['name'],
        description = value['description'],
    )


@app.put('/tasks/{item_id}')
def update_task(item_id: str, item: TaskRequest) -> None:
    r.set(f'tasks:{item_id}', json.dumps({
        'name': item.name,
        'description': item.description,
    }))


@app.post('/tasks')
def create_task(item: TaskRequest):
    item_id = str(len(tasks) + 1)
    tasks[item_id] = Task(
        item_id=item_id,
        name=item.name,
        description=item.description,
    )


def delete_tasks():
    tasks.clear()
