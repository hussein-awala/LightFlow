from enum import Enum


class TaskState(str, Enum):
    INACTIVE = "inactive"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
