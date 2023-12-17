from typing import List
from sqlalchemy.orm import Session
from app.task.models import Task, TaskCreate
from app.database.database import engine


async def create_task(task: TaskCreate) -> Task:
    """
    Create a new task using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def get_task(task_id: int) -> Task:
    """
    Retrieve a task by ID using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def get_tasks(skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Retrieve a list of tasks with optional pagination using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def update_task(task_id: int, task: Task) -> Task:
    """
    Update task information using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def delete_task(task_id: int) -> int:
    """
    Delete a task by ID using one of crud operations.
    """
    with Session(engine) as session:
        pass
