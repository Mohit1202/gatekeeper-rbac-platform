from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    operator = "operator"
    viewer = "viewer"
