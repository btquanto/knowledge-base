import time
from functools import wraps

def time_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        diff = end - start
        if diff < 1_000:
            diff = f"{diff:.0f} nanoseconds"
        elif diff < 1_000_000:
            diff = f"{diff / 1_000 :.3f} microseconds"
        elif diff < 1_000_000_000:
            diff = f"{diff / 1_000_000 :.3f} milliseconds"
        else:
            diff = f"{diff / 1_000_000_000 :.4f} seconds"
        print(f'{func.__name__} took {diff} to run')
        return result
    return wrapper