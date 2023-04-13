import time
import random
from requests.exceptions import RequestException

def retry(max_retries=3, initial_retry_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (RequestException, Exception) as e:
                    print(f"Error: {e}. Retrying...")
                    retries += 1
                    retry_delay = initial_retry_delay * (2 ** retries) * random.uniform(0.5, 1.5)
                    print(f"Waiting {retry_delay} seconds before retrying.")
                    time.sleep(retry_delay)

            raise Exception("Failed to fetch data after reaching maximum retries.")
        return wrapper
    return decorator
