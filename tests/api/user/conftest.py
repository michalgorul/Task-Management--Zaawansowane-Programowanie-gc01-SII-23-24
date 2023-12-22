from uuid import UUID

import pytest
from fastapi_pagination import Page

from app.api.user.models import BaseUser, User, UserCreate
from app.database.user.models import UserTable


@pytest.fixture
def user_id() -> UUID:
    return UUID("92e604c8-4702-48fc-9d7a-0631f4cb2b01")


@pytest.fixture
def new_user() -> BaseUser:
    return BaseUser(email="test_user@example.com", username="test_username")


@pytest.fixture
def user_create(new_user: BaseUser) -> UserCreate:
    return UserCreate(**new_user.model_dump(), password="test_password1!")


@pytest.fixture
def user(user_id: UUID, new_user: BaseUser) -> User:
    return User(user_id=user_id, **new_user.model_dump())


@pytest.fixture
def update_user() -> BaseUser:
    return BaseUser(email="test_user_new@example.com", username="test_username_new")


@pytest.fixture
def updated_user(user_id: UUID, update_user: BaseUser) -> User:
    return User(user_id=user_id, **update_user.model_dump())


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
