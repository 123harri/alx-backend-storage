#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage."""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times
    a method is called in the Cache class."""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Wrapper function that increments the call count
        and invokes the original method."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Decorator that records the call history of
    a method in the Cache class."""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Wrapper function that stores the method's
        input and output in Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, result)
        return result
    return invoker


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class method."""
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_instance = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_instance, redis.Redis):
        return
    function_name = fn.__qualname__
    input_key = f"{function_name}:inputs"
    output_key = f"{function_name}:outputs"
    call_count = 0
    if redis_instance.exists(function_name) != 0:
        call_count = int(redis_instance.get(function_name))
    print(f"{function_name} was called {call_count} times:")
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    for inp, out in zip(inputs, outputs):
        print(f"{function_name}(*{inp.decode('utf-8')}) -> {out}")


class Cache:
    """Represents an object for interacting with a Redis data store."""

    def __init__(self) -> None:
        """Initializes the Cache instance with a
        Redis client and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in the Redis data store and
        returns the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float]:
        """Retrieves a value from the Redis data store.

        Args:
            key (str): The key of the data to retrieve.
            fn (Callable, optional): A function to
            convert the data to the desired format.

        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from the Redis data store.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            str: The retrieved string.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from the Redis data store.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            int: The retrieved integer.
        """
        return self.get(key, lambda x: int(x))
