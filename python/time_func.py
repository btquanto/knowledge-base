from functools import wraps
from .timer_context import TimerContext

def time_func(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        with TimerContext(tag=func.__name__):
            result = func(*args, **kwargs)
        return result
    return wrapper
