#!/usr/bin/env python3
"""
Building a simple cache
Create a Cache class. In the __init__ method, store an instance of the Redis
"""
from typing import Callable, Optional, Union
import redis
import sys
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count number of calls made to a method"""
    key = method.__qualname__

    @wraps(method)
    def counter(self, *args, **kwargs):
        """decorator method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def history_wrapper(self, *args, **kwargs):
        """set list keys to a wrapped function"""
        in_list_key = method.__qualname__ + ":inputs"
        out_list_key = method.__qualname__ + ":outputs"
        self._redis.rpush(in_list_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_list_key, str(output))
        return output
    return history_wrapper


def replay(method: Callable) -> None:
    """function displays the history of calls of a particular function"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    server = method.__self__._redis
    count = server.get(key).decode("utf-8")
    print(f"{key} was called {count} times:")
    input_list = server.lrange(inputs, 0, -1)
    output_list = server.lrange(outputs, 0, -1)
    zipped = list(zip(input_list, output_list))
    for k, v in zipped:
        attr, result = k.decode("utf-8"), k.decode("utf-8")
        print(f"{key}(*{attr}) -> {result}")


class Cache:
    """cache class"""
    def __init__(self) -> None:
        """ Instant of Cache class """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """this method takes data argument and returns a string"""
        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return str(key)

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Union[str, bytes, int, float]:
        """retieves value from server, convert it to desired format"""
        return fn(self._redis.get(key)) if fn else self._redis.get(key)

    def get_int(self, data_bytes: bytes) -> int:
        """convert data bytes from server back to int"""
        return int.from_bytes(data_bytes, sys.byteorder)

    def get_str(self, data_bytes: bytes) -> str:
        """convert data bytes from server back into str"""
        return data_bytes.decode('utf-8')
