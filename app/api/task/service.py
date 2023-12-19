from typing import List

from sqlalchemy.orm import Session

from app.api.task.models import Task, TaskCreate


def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Service function to create a new task.
    """
    pass


def get_task(db: Session, task_id: int) -> Task:
    """
    Service function to retrieve a task by ID.
    """
    pass


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Service function to retrieve a list of tasks with optional pagination.
    """
    pass


def update_task(db: Session, task_id: int, task: Task) -> Task:
    """
    Service function to update task information.
    """
    pass


def delete_task(db: Session, task_id: int) -> int:
    """
    Service function to delete a task by ID.
    """
    pass
