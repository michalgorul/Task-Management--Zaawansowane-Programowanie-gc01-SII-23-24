from datetime import datetime, timedelta
from uuid import UUID

import pytest
from fastapi_pagination import Page
from pydantic import SecretStr

from app.api.user.models import BaseUser, User, UserCreate, UserUpdate
from app.database.user.models import UserTable


@pytest.fixture
def user_id() -> UUID:
    return UUID("92e604c8-4702-48fc-9d7a-0631f4cb2b01")


@pytest.fixture
def created_at() -> datetime:
    return datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)


@pytest.fixture
def base_user() -> BaseUser:
    return BaseUser(email="test_user@example.com", username="test_username")


@pytest.fixture
def user_create(base_user: BaseUser) -> UserCreate:
    return UserCreate(**base_user.model_dump(), password=SecretStr("test_password1!"))


@pytest.fixture
def user(user_id: UUID, base_user: BaseUser, created_at: datetime) -> User:
    return User(
        user_id=user_id,
        **base_user.model_dump(),
        created_at=created_at,
        updated_at=None
    )


@pytest.fixture
def update_user() -> UserUpdate:
    return UserUpdate(email="test_user_new@example.com", username="test_username_new")


@pytest.fixture
def updated_user(user_id: UUID, update_user: BaseUser, created_at: datetime) -> User:
    return User(
        user_id=user_id,
        **update_user.model_dump(),
        created_at=created_at,
        updated_at=created_at + timedelta(days=1)
    )


@pytest.fixture
def page() -> int:
    return 1


@pytest.fixture
def size() -> int:
    return 50


@pytest.fixture
def user_page(page: int, size: int, user: User) -> Page[User]:
    return Page(page=page, total=1, size=size, pages=1, items=[user])


@pytest.fixture
def user_table(user: User) -> UserTable:
    return UserTable(**user.model_dump())
