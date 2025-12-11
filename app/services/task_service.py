from sqlalchemy.orm import Session
from app.db.models.task import Task
from app.constants import TaskStatus
from app.core.logging_config import logger

class TaskService:
    @staticmethod
    def create_task(db: Session) -> Task:
        """
        Create a new task with status 'pending'
        """
        logger.info("Creating new task for")
        task = Task(status=TaskStatus.pending)
        db.add(task)
        db.commit()
        db.refresh(task)
        logger.info("Task created successfully")
        return task

    @staticmethod
    def get_task(db: Session, task_id: str) -> Task:
        """
        Retrieve a task by its ID
        """
        logger.info("Retrieving task with id: %s", task_id)
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task_status(
        db: Session, task_id: str, status: TaskStatus, result: str | None = None
    ) -> Task:
        """
        Update the status and optionally the result of a task
        """
        logger.info("Updating task with id: %s", task_id)
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        task.status = status
        task.result = result
        db.commit()
        db.refresh(task)
        logger.info("Task updated successfully")
        return task
