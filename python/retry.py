import time
from functools import wraps

def retry(retries=3, delay=1000):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    time.sleep(delay / 1000)
                    if attempts == retries:
                        raise e
        return wrapper
    return decorator
