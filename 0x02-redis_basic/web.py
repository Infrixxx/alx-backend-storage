#!/usr/bin/env python3
""" web.py module """


import requests
import redis
from typing import Callable
from functools import wraps


client = redis.Redis()


def url_access_count(func: Callable) -> Callable:
    """Tracks how many times a particular URL was accessed and
    cache the result with an expiration time. """
    @wraps(func)
    def wrapper(url):
        client.incr(f"count:{url}")

        content = client.get(f"result:{url}")
        if content:
            return content.decode('utf-8')

        content = func(url)
        client.set(f'count:{url}', 0)
        client.setex(f"result:{url}", 10, content)

        return content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it.
    """

    response = requests.get(url)
    html_content = response.text

    return html_content
