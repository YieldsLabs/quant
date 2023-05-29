import asyncio
import random
import time
from requests.exceptions import RequestException, ReadTimeout


def retry(max_retries=3, initial_retry_delay=1, handled_exceptions=(RequestException, ReadTimeout)):
    max_retries_exception = Exception("Failed to fetch data after reaching maximum retries.")

    async def handle_retry_async(func, *args, **kwargs):
        retries = 0

        while retries < max_retries:
            try:
                return await func(*args, **kwargs)
            except handled_exceptions as e:
                print(f"Error: {e}. Retrying...")
                retries += 1
                retry_delay = initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                print(f"Waiting {retry_delay} seconds before retrying.")
                await asyncio.sleep(retry_delay)

        raise max_retries_exception

    def handle_retry_sync(func, *args, **kwargs):
        retries = 0

        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except handled_exceptions as e:
                print(f"Error: {e}. Retrying...")
                retries += 1
                retry_delay = initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                print(f"Waiting {retry_delay} seconds before retrying.")
                time.sleep(retry_delay)

        raise max_retries_exception

    def wrapper(func):
        if asyncio.iscoroutinefunction(func):
            async def wrapped(*args, **kwargs):
                return await handle_retry_async(func, *args, **kwargs)
        else:
            def wrapped(*args, **kwargs):
                return handle_retry_sync(func, *args, **kwargs)

        return wrapped

    return wrapper
