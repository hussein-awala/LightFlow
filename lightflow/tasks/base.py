from __future__ import annotations

import abc
import logging


class BaseTask:
    task_id: str
    kwargs: dict
    logger: logging.Logger

    def __init__(self, task_id, **kwargs):
        self.task_id = task_id
        self.kwargs = kwargs
        self.logger = logging.getLogger(f"{self.__class__.__name__}/{self.task_id}")

    @abc.abstractmethod
    async def run(self, **kwargs):
        pass