import asyncio
import random
import time
from requests.exceptions import RequestException, ReadTimeout


def retry(max_retries=3, initial_retry_delay=1, handled_exceptions=(RequestException, ReadTimeout)):
    def handle_retry(func, is_async, *args, **kwargs):
        retries = 0

        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except handled_exceptions as e:
                print(f"Error: {e}. Retrying...")
                retries += 1
                retry_delay = initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                print(f"Waiting {retry_delay} seconds before retrying.")
                if is_async:
                    asyncio.sleep(retry_delay)
                else:
                    time.sleep(retry_delay)
        raise Exception("Failed to fetch data after reaching maximum retries.")

    def wrapper(func, is_async, *args, **kwargs):
        if is_async:
            async def async_wrapper():
                return await handle_retry(func, True, *args, **kwargs)
            return async_wrapper()
        else:
            return handle_retry(func, False, *args, **kwargs)

    def decorator(func):
        def wrapped(*args, **kwargs):
            return wrapper(func, asyncio.iscoroutinefunction(func), *args, **kwargs)
        return wrapped

    return decorator
