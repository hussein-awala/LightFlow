from __future__ import annotations

import abc
import logging


class BaseTask:
    task_id: str
    kwargs: dict
    logger: logging.Logger
    upstream_tasks: dict[str, BaseTask]
    downstream_tasks: dict[str, BaseTask]

    def __init__(self, task_id, **kwargs):
        self.task_id = task_id
        self.kwargs = kwargs
        self.logger = logging.getLogger(f"{self.__class__.__name__}/{self.task_id}")
        self.upstream_tasks = {}
        self.downstream_tasks = {}

    @staticmethod
    def __add_downstream(left, right, direction="LR") -> BaseTask | list[BaseTask]:
        left: list[BaseTask] = [left] if isinstance(left, BaseTask) else left
        right: list[BaseTask] = [right] if isinstance(right, BaseTask) else right
        for left_task in left:
            for right_task in right:
                if direction == "LR":
                    left_task.downstream_tasks[right_task.task_id] = right_task
                    right_task.upstream_tasks[left_task.task_id] = left_task
                else:
                    left_task.upstream_tasks[right_task.task_id] = right_task
                    right_task.downstream_tasks[left_task.task_id] = left_task
        return right

    def __rshift__(self, other: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__add_downstream(self, other, "LR")

    def __lshift__(self, other: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__add_downstream(self, other, "RL")

    def __rrshift__(self, other: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__add_downstream(other, self, "LR")

    def __rlshift__(self, other: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__add_downstream(other, self, "RL")

    def __repr__(self):
        return str({
            "task_id": self.task_id,
            "upstream_tasks": list(self.upstream_tasks.keys()),
            "downstream_tasks": list(self.downstream_tasks.keys()),
        })

    def set_downstream(self, downstream: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__rshift__(downstream)

    def set_upstream(self, upstream: BaseTask | list[BaseTask]) -> BaseTask | list[BaseTask]:
        return self.__lshift__(upstream)

    def __str__(self):
        return self.task_id

    @abc.abstractmethod
    async def run(self, **kwargs):
        pass
