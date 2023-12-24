from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


# The reason this typing error is that the type of Base is not yet inferred during semantic analysis,
# and that's when we process base classes.
class TaskTable(Base):  # type: ignore
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
