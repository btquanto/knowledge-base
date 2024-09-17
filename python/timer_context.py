import time

class TimerContext:

    def __init__(self, tag="Elapsed"):
        self.start = None
        self.tag = tag

    def __enter__(self):
        self.start = time.perf_counter_ns()
        return self

    def __exit__(self, *args):
        interval = time.perf_counter_ns() - self.start

        if interval < 1_000:
            interval = f"{interval:.0f} nanoseconds"
        elif interval < 1_000_000:
            interval = f"{interval / 1_000 :.3f} microseconds"
        elif interval < 1_000_000_000:
            interval = f"{interval / 1_000_000 :.3f} milliseconds"
        else:
            interval = f"{interval / 1_000_000_000 :.4f} seconds"

        print(f'<{self.tag}>: {interval}')
