# -*- coding: utf-8 -*-
from uuid import uuid4
from typing import Dict, List
from typing_extensions import Annotated
from os import getenv

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from redis import Redis

app = FastAPI()

def redis_client():
    return Redis(host=getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)


class TaskRequest(BaseModel):
    name: str
    description: str


class Task(TaskRequest):
    id: str


@app.get('/')
def redirect_to_tasks() -> None:
    return RedirectResponse(url='/tasks')


@app.get('/tasks')
def get_tasks(r: Annotated[Redis, Depends(redis_client)]) -> List[Task]:
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
def get_task(task_id: str, r: Annotated[Redis, Depends(redis_client)]) -> Task:
    task = r.json().get(f'tasks:{task_id}')
    return Task(
        id=task_id,
        name=task['name'],
        description=task['description'],
    )


@app.put('/tasks/{item_id}')
def update_task(task_id: str, item: TaskRequest, r: Annotated[Redis, Depends(redis_client)]) -> None:
    r.set(f'tasks:{task_id}', json.dumps({
        'name': item.name,
        'description': item.description,
    }))


@app.post('/tasks')
def create_task(request: TaskRequest, r: Annotated[Redis, Depends(redis_client)]) -> str:
    id = uuid4()
    r.json().set(f'tasks:{id}', '$', {
        'name': request.name,
        'description': request.description,
    })
    return str(id)
