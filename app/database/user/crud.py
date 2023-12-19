from typing import Any
from uuid import UUID

from fastapi_pagination import Page, Params as PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, update, delete, Row, CursorResult

from app.api.user.models import User, UserCreate, BaseUser
from app.database.database import Session
from app.database.user.models import UserTable


def create_user(user: UserCreate) -> UserTable:
    """
    Create a new user using one of crud operations.
    """
    with Session() as session:
        row = UserTable(**user.model_dump())
        session.add(row)
        session.commit()
        return row


def get_user(user_id: UUID) -> Row[tuple[UserTable]] | None:
    """
    Retrieve a user by ID using one of crud operations.
    """
    with Session() as session:
        query = select(UserTable).where(UserTable.user_id == user_id)
        return session.execute(query).fetchone()


def get_users(pagination: PaginationParams) -> Page[User]:
    """
    Retrieve a list of users with optional pagination using one of crud operations.
    """
    with Session() as session:
        paginate_user: Page[User] = paginate(session, select(UserTable), pagination)
        return paginate_user


def update_user(user_id: UUID, new_user: BaseUser) -> CursorResult[Any] | None:
    """
    Update user information using one of crud operations.
    """
    with Session() as session:
        old_user = session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if old_user:
            query = (
                update(UserTable)
                .where(UserTable.user_id == user_id)
                .values(**new_user.model_dump())
            )
            cursor = session.execute(query)
            session.commit()
            return cursor
        else:
            return None


def delete_user(user_id: UUID) -> CursorResult[Any] | None:
    """
    Delete a user by ID using one of crud operations.
    """
    with Session() as session:
        query = delete(UserTable).where(UserTable.user_id == user_id)
        cursor = session.execute(query)
        session.commit()
        return cursor
