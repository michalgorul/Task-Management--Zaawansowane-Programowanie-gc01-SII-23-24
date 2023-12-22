from typing import Any
from uuid import UUID

from fastapi_pagination import Page, Params as PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import CursorResult, Row, delete, select, update
from sqlalchemy.orm import Session

from app.api.user.models import BaseUser, User, UserCreate
from app.database.user.models import UserTable


def create_user(user: UserCreate, db: Session) -> UserTable:
    """
    Create a new user using one of crud operations.
    """
    row = UserTable(**user.model_dump())
    db.add(row)
    db.commit()
    return row


def get_user(user_id: UUID, db: Session) -> Row[tuple[UserTable]] | None:
    """
    Retrieve a user by ID using one of crud operations.
    """
    query = select(UserTable).where(UserTable.user_id == user_id)
    return db.execute(query).fetchone()


def get_users(pagination: PaginationParams, db: Session) -> Page[User]:
    """
    Retrieve a list of users with optional pagination using one of crud operations.
    """
    paginate_user: Page[User] = paginate(db, select(UserTable), pagination)
    return paginate_user


def update_user(user_id: UUID, new_user: BaseUser, db: Session) -> Row[Any] | None:
    """
    Update user information using one of crud operations.
    """
    old_user = db.query(UserTable).filter(UserTable.user_id == user_id).first()
    if old_user:
        query = (
            update(UserTable)
            .where(UserTable.user_id == user_id)
            .values(**new_user.model_dump())
        )
        cursor = db.execute(query)
        db.commit()
        return cursor.fetchone()
    else:
        return None


def delete_user(user_id: UUID, db: Session) -> CursorResult[Any] | None:
    """
    Delete a user by ID using one of crud operations.
    """
    query = delete(UserTable).where(UserTable.user_id == user_id)
    cursor = db.execute(query)
    db.commit()
    return cursor
