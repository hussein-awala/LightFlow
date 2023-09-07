from __future__ import annotations

import asyncio
import random

from lightflow.jobs.base import BaseJob
from lightflow.tasks.test_task import TestTask
from lightflow.jobs.executor import Executor


class Scheduler(BaseJob):
    job_name = "Scheduler"
    executor: Executor

    def __init__(self):
        super().__init__()
        self.executor = Executor()

    async def schedule_tasks(self):
        self.logger.debug(f"schedule_tasks started")
        for i in range(10000):
            test_task = TestTask(i, sleep_time=random.randint(5, 20))
            self.executor.queued_tasks.append(test_task)
            self.logger.debug(f"Task {test_task.task_id} scheduled")
            await asyncio.sleep(0.5)

    async def run(self):
        await asyncio.gather(self.schedule_tasks(), self.executor.run())
