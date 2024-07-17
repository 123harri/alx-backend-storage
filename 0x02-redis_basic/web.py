#!/usr/bin/env python3
"""
A module with tools for request caching and tracking using Redis.
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize a module-level Redis instance
redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    """
    Decorator that caches the output of fetched
    data and tracks the number of requests.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with caching and tracking functionality.
    """
    @wraps(method)
    def invoker(url: str) -> str:
        """
        Wrapper function for caching fetched data and tracking requests.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            str: The content fetched from the URL.
        """
        # Increment the request count for the URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is already cached
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # Fetch the data and cache the result
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Fetches the content of a URL, caches the
    response, and tracks the request count.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        str: The content fetched from the URL.
    """
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
