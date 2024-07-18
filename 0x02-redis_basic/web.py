#!/usr/bin/env python3
"""
Module for fetching web pages and caching results.
"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def track_requests(method: Callable) -> Callable:
    """
    Decorator function to track the number of requests for each URL.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that tracks requests and caches results.
        """
        redis_client.incr(f"count:{url}")

        cached_result = redis_client.get(f"result:{url}")
        if cached_result:
            return cached_result.decode('utf-8')

        result = method(url)

        redis_client.setex(f"result:{url}", 10, result)

        return result

    return wrapper


@track_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content from a URL and returns it.
    """
    response = requests.get(url)
    return response.text
