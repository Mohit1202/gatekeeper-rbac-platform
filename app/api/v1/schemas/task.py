from pydantic import BaseModel

from app.constants import TaskStatus


class TaskRead(BaseModel):
    id: int
    status: TaskStatus
    result: str | None

    model_config = {"from_attributes": True}
