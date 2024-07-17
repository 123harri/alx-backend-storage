#!/usr/bin/env python3
"""
A module for fetching and caching web pages using Redis.
"""
import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_page(func: Callable) -> Callable:
    """Decorator to cache web page content and track access count."""
    @wraps(func)
    def wrapper(url: str) -> str:
        """Wrapper function that manages caching and tracking."""
        cache_key = f"count:{url}"
        content_key = f"content:{url}"

        redis_client.incr(cache_key)

        cached_content = redis_client.get(content_key)
        if cached_content:
            return cached_content.decode('utf-8')

        content = func(url)
        redis_client.setex(content_key, 10, content)

        return content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    response = requests.get(url)
    return response.text
