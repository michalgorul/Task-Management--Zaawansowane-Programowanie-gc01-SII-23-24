from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params as PaginationParams
from sqlalchemy.orm import Session

from app.api.task import service
from app.api.task.models import Task, TaskCreate, TaskUpdate
from app.database.database import get_db

router = APIRouter(prefix="/tasks", tags=["Task Management"])


@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate, db: Annotated[Session, Depends(get_db)]
) -> Task:
    return await service.create_task(task, db)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Task:
    return await service.get_task(task_id, db)


@router.get("/", response_model=Page[Task])
async def get_tasks(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
) -> Page[Task]:
    return await service.get_tasks(pagination, db)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID, new_task: TaskUpdate, db: Annotated[Session, Depends(get_db)]
) -> Task:
    return await service.update_task(task_id=task_id, new_task=new_task, db=db)


@router.delete("/{task_id}", response_model=UUID)
async def delete_task(task_id: UUID, db: Annotated[Session, Depends(get_db)]) -> int:
    return await service.delete_task(task_id, db)
