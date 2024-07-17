#!/usr/bin/env python3
"""
A simple caching mechanism for web requests using Redis.
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize a Redis client
redis_store = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator that counts requests and caches their responses."""

    @wraps(method)
    def wrapper(url):
        """Wrapper function to handle request counting and caching."""

        # Increment the request count for the URL
        rd.incr(f"count:{url}")

        # Check if the result is already cached
        cached_html = rd.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # Fetch the HTML content from the URL
        html = method(url)

        # Cache the fetched HTML content with a 10-second expiration
        rd.setex(f"cached:{url}", 10, html)

        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Fetches the HTML content from a given URL."""
    req = requests.get(url)
    return req.text
