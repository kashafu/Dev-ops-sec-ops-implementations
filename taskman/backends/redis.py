
from .backend import Backend
from os import getenv
from redis import Redis

class RedisBackend(Backend):
    def __init__(self)-> None:
        self.redis = Redis(host=getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)

    def keys():
        return self.redis.keys()
