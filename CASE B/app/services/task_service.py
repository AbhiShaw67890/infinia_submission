"""
Task CRUD service layer.
Handles all database operations for tasks.
"""

import logging
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


def get_tasks(db: Session, completed: bool | None = None) -> list[Task]:
    """Retrieve all tasks, optionally filtered by completion status."""
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.order_by(Task.created_at.desc()).all()


def get_task(db: Session, task_id: int) -> Task | None:
    """Retrieve a single task by ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """Create a new task."""
    task = Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info("task_created id=%d title='%s'", task.id, task.title)
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task | None:
    """Update an existing task. Returns None if not found."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None

    update_fields = task_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    logger.info("task_updated id=%d fields=%s", task.id, list(update_fields.keys()))
    return task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task. Returns True if deleted, False if not found."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return False

    db.delete(task)
    db.commit()
    logger.info("task_deleted id=%d", task_id)
    return True
