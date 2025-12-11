from sqlalchemy import Column, String, Enum, Integer

from app.constants import TaskStatus
from app.db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    result = Column(String, nullable=True)
