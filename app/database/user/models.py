from typing import Any, Dict
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column

from app.database.models import Base


class UserTable(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    ...

    def dict(self) -> Dict[str, Any]:
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d
