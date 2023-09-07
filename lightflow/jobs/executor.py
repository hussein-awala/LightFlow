from __future__ import annotations

import asyncio
from collections import deque
from typing import TYPE_CHECKING

from lightflow.jobs.base import BaseJob
if TYPE_CHECKING:
    from lightflow.tasks.base import BaseTask


class Executor(BaseJob):
    job_name = "Executor"
    queued_tasks: deque[BaseTask] = deque()
    running_tasks = {}
    finished_tasks = {}

    async def execute_tasks(self):
        self.logger.debug(f"execute_tasks started")
        while not self.stopped:
            if not self.queued_tasks:
                self.logger.debug("No tasks to execute, sleeping for 1 second")
                await asyncio.sleep(1)
                continue
            task = self.queued_tasks.pop()
            self.running_tasks[task.task_id] = asyncio.create_task(task.run(**task.kwargs))
            self.logger.debug(f"Task {task.task_id} started")
            await asyncio.sleep(0)
        self.logger.debug("Executor stopped")

    async def clean_finished_tasks_tasks(self):
        self.logger.debug("clean_finished_tasks_tasks started")
        while not self.stopped:
            if not self.running_tasks:
                self.logger.debug("No tasks to clean, sleeping for 1 second")
                await asyncio.sleep(1)
                continue
            for task_id, task in list(self.running_tasks.items()):
                if task.done():
                    self.finished_tasks[task_id] = task.result()
                    del self.running_tasks[task_id]
                    self.logger.debug(f"Task {task_id} finished_tasks with result {self.finished_tasks[task_id]}")
                await asyncio.sleep(0)
            await asyncio.sleep(1)
        self.logger.debug("Executor stopped")

    async def run(self):
        await asyncio.gather(self.execute_tasks(), self.clean_finished_tasks_tasks())
