from typing import List

from fastapi import APIRouter

from app.task.models import Task, TaskCreate

router = APIRouter(prefix="", tags=["Task Management"])


@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate) -> Task:
    pass


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    pass


@router.get("/tasks/", response_model=List[Task])
async def get_tasks(skip: int = 0, limit: int = 100) -> List[Task]:
    pass


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task) -> Task:
    pass


@router.delete("/tasks/{task_id}", response_model=int)
async def delete_task(task_id: int) -> int:
    pass
