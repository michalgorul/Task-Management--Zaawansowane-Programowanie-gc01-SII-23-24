import logging
from uuid import UUID

from fastapi import HTTPException
from fastapi_pagination import Page, Params as PaginationParams
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.user.models import (
    BaseUser,
    User,
    UserCreate,
    UserResponse,
    UserTasks,
    UserUpdate,
)
from app.database.user import crud

logger = logging.getLogger(__name__)

USER_NOT_FOUND = (404, "User not found")


async def create_user(user: UserCreate, db: Session) -> UserResponse:
    """
    Service function to create a new user.
    """
    try:
        db_user = crud.create_user(user, db)
    except IntegrityError as ie:
        error_str = f"Failed to add row to table, data={user.model_dump()}, error={ie}"
        logger.error(error_str)
        raise HTTPException(status_code=409, detail=str(ie))
    except Exception as e:
        error_str = f"Failed to add row to table, data={user.model_dump()}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return UserResponse.model_validate(db_user)


async def get_user(user_id: UUID, db: Session) -> UserResponse:
    """
    Service function to retrieve a user by ID.
    """
    db_user = crud.get_user(user_id, db)
    if db_user:
        try:
            return UserResponse.model_validate(db_user[0])
        except Exception as e:
            error_str = f"Failed to get User, user_id={user_id}, error={e}"
            logger.error(error_str)
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(*USER_NOT_FOUND)


async def get_user_tasks(user_id: UUID, db: Session) -> UserTasks:
    """
    Service function to retrieve a user by ID.
    """
    db_user_tasks = crud.get_user(user_id, db)
    if db_user_tasks:
        try:
            return UserTasks.model_validate(db_user_tasks[0])
        except Exception as e:
            error_str = f"Failed to get User tasks, user_id={user_id}, error={e}"
            logger.error(error_str)
            raise HTTPException(status_code=500, detail=str(e))
    raise HTTPException(*USER_NOT_FOUND)


async def get_users(pagination: PaginationParams, db: Session) -> Page[UserResponse]:
    """
    Service function to retrieve a list of users with optional pagination.
    """
    return crud.get_users(pagination, db)


async def update_user(user_id: UUID, new_user: UserUpdate, db: Session) -> UserResponse:
    """
    Service function to update user information.
    """
    try:
        updated_user = crud.update_user(user_id=user_id, new_user=new_user, db=db)
    except Exception as e:
        error_str = f"Failed to update User, user_id={user_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))

    if updated_user:
        logger.info(f"Updated user, user_id={user_id}, new_user={new_user}")
        return await get_user(user_id, db)
    raise HTTPException(*USER_NOT_FOUND)


async def delete_user(user_id: UUID, db: Session) -> UUID:
    """
    Service function to delete a user by ID.
    """
    existing_user = await get_user(user_id, db)
    if existing_user is None:
        raise HTTPException(*USER_NOT_FOUND)

    try:
        crud.delete_user(user_id, db)
    except Exception as e:
        error_str = f"Failed to delete User, user_id={user_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return user_id
