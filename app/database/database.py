from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.config import settings

db_user: str = settings.db_user
db_password: str = settings.db_password
db_host: str = settings.db_host
db_port: str = settings.db_port
db_database: str = settings.db_database

db_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"

engine = create_engine(url=db_string, echo=True)

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine, expire_on_commit=False)

# SqlAlchemy ORM model
Base = declarative_base()
