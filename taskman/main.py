# -*- coding: utf-8 -*-
from uuid import uuid4
from typing import List
from os import getenv
from typing_extensions import Annotated

from fastapi import Depends, FastAPI
from starlette.responses import RedirectResponse
from .backends import Backend, RedisBackend
from .model import Task, TaskRequest

app = FastAPI()


def get_backend() -> Backend:
    backend_type = getenv('BACKEND', 'redis')
    if backend_type == 'redis':
        return RedisBackend()
    else:
        return null

@app.get('/')
def redirect_to_tasks() -> None:
    return RedirectResponse(url='/tasks')


@app.get('/tasks')
def get_tasks(backend: Annotated[Backend, Depends(get_backend())]) -> List[Task]:
    keys = backend.keys()

    tasks = []
    for key in keys:
        task = redis.json().get(key)
        task_id = key[6:]
        tasks.append(Task(
            id=task_id,
            name=task['name'],
            description=task['description'],
        ))
    return tasks


@app.get('/tasks/{task_id}')
def get_task(task_id: str,
             backend: Annotated[Backend, Depends(get_backend())]) -> Task:
    task = redis.json().get(f'tasks:{task_id}')
    return Task(
        id=task_id,
        name=task['name'],
        description=task['description'],
    )


@app.put('/tasks/{item_id}')
def update_task(task_id: str,
                item: TaskRequest,
                redis: Annotated[Redis, Depends(redis_client)]) -> None:
    redis.json().set(f'tasks:{task_id}', {
        'name': item.name,
        'description': item.description,
    })


@app.post('/tasks')
def create_task(request: TaskRequest,
                backend: Annotated[Backend, Depends(get_backend())]) -> str:
    task_id = uuid4()
    redis.json().set(f'tasks:{task_id}', '$', {
        'name': request.name,
        'description': request.description,
    })
    return str(task_id)
