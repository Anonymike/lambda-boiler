import redis
import time


class RedisConnection(object):
    def __init__(self, host, port):
        self.db = redis.StrictRedis(
            host=host, port=port, charset='utf-8',
            decode_responses=True)

    def _redis_format(self, obj):
        if isinstance(obj, bool):
            return str(obj).lower()
        if isinstance(obj, (list, tuple)):
            return [self._redis_format(item) for item in obj]
        if isinstance(obj, dict):
            return {self._redis_format(key): self._redis_format(value) for key, value in obj.items()}
        return obj

    def insert_key(self, key, value, expire=None):
        self.db.hmset(key, value)
        if expire:
            self.db.expire(key, expire)

    def get_value(self, key):
        return self.db.hgetall(key)
