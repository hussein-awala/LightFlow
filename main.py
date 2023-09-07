import asyncio
import logging

from lightflow.jobs.scheduler import Scheduler

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
    scheduler = Scheduler()
    asyncio.run(scheduler.run())
