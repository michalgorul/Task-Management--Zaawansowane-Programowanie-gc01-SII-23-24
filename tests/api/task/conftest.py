from datetime import datetime, timedelta
from uuid import UUID

import pytest
from fastapi_pagination import Page

from app.api.task.models import BaseTask, Task, TaskCreate, TaskUpdate
from app.database.task.models import TaskTable


@pytest.fixture
def task_id() -> UUID:
    return UUID("b6459e03-6b6d-4bd7-8b97-e766472bc403")


@pytest.fixture
def base_task(user_id: UUID) -> BaseTask:
    return BaseTask(name="Test name", description="Test description", user_id=user_id)


@pytest.fixture
def task_create(base_task: BaseTask) -> TaskCreate:
    return TaskCreate(**base_task.model_dump())


@pytest.fixture
def task(task_id: UUID, base_task: BaseTask, created_at: datetime) -> Task:
    return Task(
        task_id=task_id,
        **base_task.model_dump(),
        created_at=created_at,
        updated_at=None,
    )


@pytest.fixture
def update_task() -> TaskUpdate:
    return TaskUpdate(name="Test name new", description="Test description new")


@pytest.fixture
def updated_task(
    task_id: UUID, update_task: TaskUpdate, created_at: datetime, user_id: UUID
) -> Task:
    return Task(
        task_id=task_id,
        **update_task.model_dump(),
        created_at=created_at,
        updated_at=created_at + timedelta(days=1),
        user_id=user_id,
    )


@pytest.fixture
def task_page(page: int, size: int, task: Task) -> Page[Task]:
    return Page(page=page, total=1, size=size, pages=1, items=[task])


@pytest.fixture
def task_table(task: Task) -> TaskTable:
    return TaskTable(**task.model_dump())
