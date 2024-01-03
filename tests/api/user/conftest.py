from datetime import datetime, timedelta
from uuid import UUID

import pytest
from fastapi_pagination import Page
from pydantic import SecretStr

from app.api.task.models import TaskWithoutUser
from app.api.user.models import (
    BaseUser,
    User,
    UserCreate,
    UserResponse,
    UserTasks,
    UserUpdate,
)
from app.database.task.models import TaskTable
from app.database.user.models import UserTable


@pytest.fixture
def base_user() -> BaseUser:
    return BaseUser(email="test_user@example.com", username="test_username")


@pytest.fixture
def user_create(base_user: BaseUser) -> UserCreate:
    return UserCreate(**base_user.model_dump(), password=SecretStr("test_password1!"))


@pytest.fixture
def user_response(
    user_id: UUID, base_user: BaseUser, created_at: datetime
) -> UserResponse:
    return UserResponse(
        user_id=user_id,
        **base_user.model_dump(),
        created_at=created_at,
        updated_at=None,
    )


@pytest.fixture
def update_user() -> UserUpdate:
    return UserUpdate(email="test_user_new@example.com", username="test_username_new")


@pytest.fixture
def updated_user(user_id: UUID, update_user: UserUpdate, created_at: datetime) -> User:
    return User(
        user_id=user_id,
        **update_user.model_dump(),
        created_at=created_at,
        updated_at=created_at + timedelta(days=1),
        tasks=[],
    )


@pytest.fixture
def user_page(page: int, size: int, user_response: User) -> Page[User]:
    return Page(page=page, total=1, size=size, pages=1, items=[user_response])


@pytest.fixture
def user_table(user_response: User) -> UserTable:
    return UserTable(**user_response.model_dump())


@pytest.fixture
def task_without_user(created_at: datetime) -> TaskWithoutUser:
    return TaskTable(
        name="Test name",
        description="Test description",
        task_id="fe8d85be-c813-492b-86f4-2739550beb1a",
        created_at=created_at,
        updated_at=None,
    )


@pytest.fixture
def task_with_user(created_at: datetime, user_id: UUID) -> TaskWithoutUser:
    return TaskTable(
        name="Test name",
        description="Test description",
        task_id="fe8d85be-c813-492b-86f4-2739550beb1a",
        created_at=created_at,
        updated_at=None,
        user_id=user_id,
    )


@pytest.fixture
def users_tasks(user_id: UUID, task_without_user: TaskWithoutUser) -> UserTasks:
    return UserTasks(user_id=user_id, tasks=[task_without_user])


@pytest.fixture
def user_table_with_tasks(user_response: User, task_with_user: TaskTable) -> UserTable:
    return UserTable(**user_response.model_dump() | {"tasks": [task_with_user]})
