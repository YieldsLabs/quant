import asyncio
import random
from requests.exceptions import RequestException

def retry(max_retries=3, initial_retry_delay=1):
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (RequestException, Exception) as e:
                    print(f"Error: {e}. Retrying...")
                    retries += 1
                    retry_delay = initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                    print(f"Waiting {retry_delay} seconds before retrying.")
                    await asyncio.sleep(retry_delay)

            raise Exception("Failed to fetch data after reaching maximum retries.")
        return async_wrapper
    return decorator
