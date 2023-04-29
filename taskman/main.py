# -*- coding: utf-8 -*-
from uuid import uuid4
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import redis

app = FastAPI()

r = redis.Redis(host='redis', port=6379, decode_responses=True)


class TaskRequest(BaseModel):
    name: str
    description: str


class Task(TaskRequest):
    id: str


tasks: Dict[str, Task] = {}


@app.get('/')
def redirect_to_tasks() -> None:
    return RedirectResponse(url='/tasks')


@app.get('/tasks')
def get_tasks() -> List[Task]:
    keys = r.keys()

    tasks = []
    for key in keys:
        task = r.json().get(key)
        id = key[6:]
        tasks.append(Task(
            id=id,
            name=task['name'],
            description=task['description'],
        ))
    return tasks


@app.get('/tasks/{task_id}')
def get_task(task_id: str) -> Task:
    task = r.json().get(f'tasks:{task_id}')
    return Task(
        id=task_id,
        name=task['name'],
        description=task['description'],
    )


@app.put('/tasks/{item_id}')
def update_task(task_id: str, item: TaskRequest) -> None:
    r.set(f'tasks:{task_id}', json.dumps({
        'name': item.name,
        'description': item.description,
    }))


@app.post('/tasks')
def create_task(request: TaskRequest):
    id = uuid4()
    r.json().set(f'tasks:{id}', '$', {
        'name': request.name,
        'description': request.description,
    })


def delete_tasks():
    tasks.clear()
