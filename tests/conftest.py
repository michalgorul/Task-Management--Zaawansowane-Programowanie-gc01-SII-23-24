import os
from typing import Generator

import pytest
from sqlalchemy.orm import Session

os.environ["USE_CACHED_SETTINGS"] = "False"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_DATABASE"] = "test"


@pytest.fixture
def db() -> Generator[Session, None, None]:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db is not None:
            db.close()
