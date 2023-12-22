from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app.config import get_settings

settings = get_settings()

db_user: str = settings.db_user
db_password: str = settings.db_password
db_host: str = settings.db_host
db_port: str = settings.db_port
db_database: str = settings.db_database

db_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"

engine = create_engine(url=db_string, echo=True)

if not database_exists(engine.url):
    create_database(engine.url)

print(engine.url)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


# SqlAlchemy ORM model
Base = declarative_base()
