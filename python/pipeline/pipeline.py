"""
Example:
```
    pipeline = Pipeline()

    stage = Stage(lambda x: x + 1) # 1 + 1 = 2
    pipeline.add_stage(stage)

    parallel_stage = ParallelStage()
    parallel_stage.add_branch(Stage(lambda x: x + 1)) # 2 + 1 = 3
    parallel_stage.add_branch(Stage(lambda x: x + 2)) # 2 + 2 = 4

    pipeline.add_stage(parallel_stage)

    stage = Stage(lambda x, y: x + y)  # 3 + 4 = 7
    pipeline.add_stage(stage)

    print(pipeline(1)) # Input: x = 1, return 7
```
"""

import os
from concurrent.futures import Executor, ThreadPoolExecutor


class Stage:

    def __init__(self, func: callable):
        self.func : callable = func

    def __call__(self, *args):
        return self.func(*args)


class ParallelStage(Stage):

    def __init__(self, executor: Executor = None, max_workers=None, **executor_kwargs):
        self.branches : list[Stage] = []
        if executor is None:
            executor = ThreadPoolExecutor
        self.executor : Executor = executor
        if max_workers is None:
            max_workers = os.cpu_count()
        self.executor_kwargs = {
            'max_workers': max_workers,
            **executor_kwargs
        }

    def add_branch(self, stage):
        self.branches.append(stage)

    def __call__(self, *args):
        with self.executor(**self.executor_kwargs) as executor:
            futures = [executor.submit(branch, *args) for branch in self.branches]
            results = [future.result() for future in futures]
        return results


class Pipeline:

    def __init__(self):
        self.stages : list[Stage] = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def __call__(self, *args):
        if not self.stages:
            return
        results = self.stages[0](*args)
        for stage in self.stages[1:]:
            if not isinstance(results, (list, tuple)):
                results = [results]
            results = stage(*results)
        return results
