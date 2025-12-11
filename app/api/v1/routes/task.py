import time

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.task_service import TaskService
from app.core.security import get_current_active_user
from app.api.v1.dependencies.auth import validate_roles
from app.api.v1.schemas.task import TaskRead
from fastapi import HTTPException
from app.constants import TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


def run_task(db: Session, task_id: str):
    TaskService.update_task_status(db, task_id, TaskStatus.running)
    try:
        time.sleep(15)
        TaskService.update_task_status(
            db,
            task_id,
            TaskStatus.completed,
            result=f"Task {task_id} completed successfully",
        )
    except Exception as e:
        TaskService.update_task_status(db, task_id, TaskStatus.failed, result=str(e))


@router.post("/execute", response_model=TaskRead)
async def execute_task(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _=Depends(validate_roles(["manager"])),
):
    task = TaskService.create_task(db)
    background_tasks.add_task(run_task, db, task.id)
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_status(
    task_id: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)
):
    task = TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
