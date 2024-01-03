from typing import Any
from uuid import UUID

from fastapi_pagination import Page, Params as PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import CursorResult, Row, delete, select, update
from sqlalchemy.orm import Session

from app.api.task.models import Task, TaskCreate, TaskUpdate
from app.database.task.models import TaskTable


def create_task(task: TaskCreate, db: Session) -> TaskTable:
    """
    Create a new task using one of crud operations.
    """
    row = TaskTable(**task.model_dump())
    db.add(row)
    db.commit()
    return row


def get_task(task_id: UUID, db: Session) -> Row[tuple[TaskTable]] | None:
    """
    Retrieve a task by ID using one of crud operations.
    """
    query = select(TaskTable).where(TaskTable.task_id == task_id)
    return db.execute(query).fetchone()


def get_tasks(pagination: PaginationParams, db: Session) -> Page[Task]:
    """
    Retrieve a list of tasks with optional pagination using one of crud operations.
    """
    paginate_task: Page[Task] = paginate(db, select(TaskTable), pagination)
    return paginate_task


def update_task(
    task_id: UUID, new_task: TaskUpdate, db: Session
) -> CursorResult[int] | None:
    """
    Update task information using one of crud operations.
    """
    old_task = db.query(TaskTable).filter(TaskTable.task_id == task_id).first()
    if old_task:
        query = (
            update(TaskTable)
            .where(TaskTable.task_id == task_id)
            .values(**new_task.model_dump(exclude_unset=True))
        )
        cursor = db.execute(query)
        db.commit()
        return cursor
    else:
        return None


def delete_task(task_id: UUID, db: Session) -> CursorResult[Any] | None:
    """
    Delete a task by ID using one of crud operations.
    """
    query = delete(TaskTable).where(TaskTable.task_id == task_id)
    cursor = db.execute(query)
    db.commit()
    return cursor
