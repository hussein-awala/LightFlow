from __future__ import annotations

import asyncio
from lightflow.tasks.base import BaseTask


class TestTask(BaseTask):
    async def run(self, sleep_time: int):
        self.logger.debug(self.task_id)
        await asyncio.sleep(sleep_time)
        return sleep_time
