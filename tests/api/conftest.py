from datetime import datetime
from typing import Generator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def user_id() -> UUID:
    return UUID("92e604c8-4702-48fc-9d7a-0631f4cb2b01")


@pytest.fixture
def created_at() -> datetime:
    return datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)


@pytest.fixture
def page() -> int:
    return 1


@pytest.fixture
def size() -> int:
    return 50
