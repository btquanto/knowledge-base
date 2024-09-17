"""
Example:
```
    with Pipeline() as pipeline:
        pipeline.add_stage(lambda x: x + 1) # 1 + 1 = 2
        pipeline.add_parallel_stage(
            lambda x: x + 1, # 2 + 1 = 3
            lambda x: x + 2  # 2 + 2 = 4
        )
        pipeline.add_stage(lambda x, y: x + y) # 3 + 4 = 7

        print(pipeline(1)) # Input: x = 1, return 7
```
"""

import os
from typing import Callable
from concurrent.futures import Executor, ThreadPoolExecutor


class Stage:

    def __init__(self, func: Callable):
        self.func : Callable = func

    def __call__(self, *args):
        return self.func(*args)


class ParallelStage(Stage):

    def __init__(self, executor: Executor = None):
        self.branches : list[Stage] = []
        self.executor : Executor = executor

    def add_branch(self, stage : Stage | Callable):
        if not isinstance(stage, Stage):
            stage = Stage(stage)
        self.branches.append(stage)

    def __call__(self, *args):
        futures = [self.executor.submit(branch, *args) for branch in self.branches]
        results = [future.result() for future in futures]
        return results


class Pipeline:

    def __init__(self, executor: Executor = None, max_workers=None, **executor_kwargs):
        self.stages : list[Stage] = []
        if executor is None:
            executor = ThreadPoolExecutor
        if max_workers is None:
            max_workers = os.cpu_count()
        self.executor = executor(max_workers=max_workers, **executor_kwargs)

    def __enter__(self):
        self.executor.__enter__()
        return self

    def __exit__(self, *args):
        return self.executor.__exit__(*args)

    def add_stage(self, stage: Stage | Callable):
        if not isinstance(stage, Stage):
            stage = Stage(stage)
        self.stages.append(stage)

    def add_parallel_stage(self, *stages: list[Stage | Callable]):
        parallel_stage = ParallelStage(self.executor)
        for stage in stages:
            parallel_stage.add_branch(stage)
        self.add_stage(parallel_stage)

    def __call__(self, *args):
        if not self.stages:
            return
        results = self.stages[0](*args)
        for stage in self.stages[1:]:
            if not isinstance(results, (list, tuple)):
                results = [results]
            results = stage(*results)
        return results
