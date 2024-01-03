from uuid import uuid4

from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


# The reason this typing error is that the type of Base is not yet inferred during semantic analysis,
# and that's when we process base classes.
class UserTable(Base):  # type: ignore
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    username = Column(String(), unique=True)
    email = Column(String(), unique=True)
    password = Column(String())
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    tasks = relationship("TaskTable", back_populates="user", lazy="selectin")
