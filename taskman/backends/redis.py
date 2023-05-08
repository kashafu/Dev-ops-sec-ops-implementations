# -*- coding: utf-8 -*-
from os import getenv

from redis import Redis
from taskman import Task, TaskRequest
from .backend import Backend


class RedisBackend(Backend):
    def __init__(self) -> None:
        self.redis = Redis(host=getenv('REDIS_HOST', 'localhost'),
                           port=6379, decode_responses=True)

    def keys(self) -> list[str]:
        return self.redis.keys()

    def get(self, task_id: str) -> Task:
        task = self.redis.json().get(task_id)
        return Task(
            id=task_id[6:],
            name=task['name'],
            description=task['description'],
        )

    def set(self, task_id: str, request: TaskRequest):
        self.redis.json().set(f'tasks:{task_id}', '$', {
            'name': request.name,
            'description': request.description,
        })
