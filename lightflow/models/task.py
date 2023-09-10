from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, Enum, func, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from lightflow.metadata.session import provide_async_session
from lightflow.models.base import BaseModel
from lightflow.observability.sql_logger import sql_logger
from lightflow.state import TaskState

if TYPE_CHECKING:
    from lightflow.tasks.base import BaseTask


class TaskModel(BaseModel):
    """The task model."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(255), nullable=False)
    state = Column(Enum(TaskState), nullable=False, default=TaskState.INACTIVE)
    started_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    @staticmethod
    @provide_async_session
    async def init_task(task: BaseTask, async_session: AsyncSession = None) -> int:
        """Initialize a task in the database.

        This method will create a new task in the database from the given task,
        and return the id of the newly created task.

        :arg task: The task to initialize.
        :arg async_session: The async session to use for the database operations.
        :return: The id of the newly created task.
        """
        insert_stmt = (
            insert(TaskModel)
            .values(task_id=task.task_id, state=TaskState.INACTIVE)
            .returning(TaskModel.id)
        )
        sql_logger.info(str(insert_stmt))
        return (await async_session.execute(insert_stmt)).scalar_one().id

    @staticmethod
    @provide_async_session
    async def get_task(task_id: str, async_session: AsyncSession = None) -> TaskModel:
        """Get a task from the database.

        This method will retrieve a task from the database based on the given
        task id.

        :arg task_id: The id of the task to retrieve.
        :arg async_session: The async session to use for the database operations.
        :return: The task model.
        """
        select_stmt = select(TaskModel).where(TaskModel.task_id == task_id)
        sql_logger.info(str(select_stmt))
        return (await async_session.execute(select_stmt)).scalar_one()
