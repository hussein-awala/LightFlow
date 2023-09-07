from __future__ import annotations

import abc
import logging
import uuid


class BaseJob:
    job_id: uuid.UUID
    job_name: str = "BaseJob"
    logger: logging.Logger
    stopped: bool = False

    def __init__(self):
        self.job_id = uuid.uuid4()
        self.logger = logging.getLogger(f"{self.job_name}/{self.job_id}")

    async def stop(self):
        self.stopped = True

    @abc.abstractmethod
    async def run(self):
        pass
