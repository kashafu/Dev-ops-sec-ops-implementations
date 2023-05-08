from abc import ABC, abstractmethod

class Backend(ABC):

    @abstractmethod
    def keys():
        return []
