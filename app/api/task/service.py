import logging
from uuid import UUID

from fastapi import HTTPException
from fastapi_pagination import Page, Params as PaginationParams
from sqlalchemy.orm import Session

from app.api.task.models import Task, TaskCreate, TaskUpdate
from app.database.task import crud

logger = logging.getLogger(__name__)

TASK_NOT_FOUND = (404, "Task not found")


async def create_task(task: TaskCreate, db: Session) -> Task:
    """
    Service function to create a new task.
    """
    try:
        db_task = crud.create_task(task, db)
    except Exception as e:
        error_str = f"Failed to add row to table, data={task.model_dump()}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return Task.model_validate(db_task)


async def get_task(task_id: UUID, db: Session) -> Task:
    """
    Service function to retrieve a task by ID.
    """
    db_task = crud.get_task(task_id, db)
    if db_task:
        try:
            return Task.model_validate(db_task[0])
        except Exception as e:
            error_str = f"Failed to get Task, task_id={task_id}, error={e}"
            logger.error(error_str)
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(*TASK_NOT_FOUND)


async def get_tasks(pagination: PaginationParams, db: Session) -> Page[Task]:
    """
    Service function to retrieve a list of tasks with optional pagination.
    """
    return crud.get_tasks(pagination, db)


async def update_task(task_id: UUID, new_task: TaskUpdate, db: Session) -> Task:
    """
    Service function to update task information.
    """
    try:
        updated_user = crud.update_task(task_id=task_id, new_task=new_task, db=db)
    except Exception as e:
        error_str = f"Failed to update Task, task_id={task_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))

    if updated_user:
        logger.info(f"Updated user, user_id={task_id}, new_user={new_task}")
        return await get_task(task_id, db)
    raise HTTPException(*TASK_NOT_FOUND)


async def delete_task(task_id: UUID, db: Session) -> UUID:
    """
    Service function to delete a task by ID.
    """
    existing_task = await get_task(task_id, db)
    if existing_task is None:
        raise HTTPException(*TASK_NOT_FOUND)

    try:
        crud.delete_task(task_id, db)
    except Exception as e:
        error_str = f"Failed to delete Task, task_id={task_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return task_id
