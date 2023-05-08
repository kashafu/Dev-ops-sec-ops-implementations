# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from taskman import TaskRequest


class Backend(ABC):

    @abstractmethod
    def keys(self) -> list[str]:
        pass

    @abstractmethod
    def get(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def set(self, task_id: str, request: TaskRequest):
        pass
