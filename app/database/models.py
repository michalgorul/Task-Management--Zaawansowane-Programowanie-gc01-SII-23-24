from sqlalchemy.ext.declarative import declarative_base

from app.models import BaseModel

# SqlAlchemy ORM model
Base = declarative_base()


# Pydantic ORM model
class SchemaModel(BaseModel):
    class Config:
        orm_mode = True
