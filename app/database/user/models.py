from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


# The reason this typing error is that the type of Base is not yet inferred during semantic analysis,
# and that's when we process base classes.
class UserTable(Base):  # type: ignore
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    username = Column(String(), unique=True)
    email = Column(String(), unique=True)
    password = Column(String())
