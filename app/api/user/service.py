import logging
from uuid import UUID

from fastapi import HTTPException
from fastapi_pagination import Page, Params as PaginationParams

from app.api.user.models import User, UserCreate, BaseUser
from app.database.user import crud

logger = logging.getLogger(__name__)

USER_NOT_FOUND = (404, "User not found")


async def create_user(user: UserCreate) -> User:
    """
    Service function to create a new user.
    """
    try:
        db_user = crud.create_user(user)
    except Exception as e:
        error_str = f"Failed to add row to table, data={user.model_dump()}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return User.model_validate(db_user)


async def get_user(user_id: UUID) -> User:
    """
    Service function to retrieve a user by ID.
    """
    db_user = crud.get_user(user_id)
    if db_user:
        return User.model_validate(db_user[0])
    raise HTTPException(*USER_NOT_FOUND)


async def get_users(pagination: PaginationParams) -> Page[User]:
    """
    Service function to retrieve a list of users with optional pagination.
    """
    return crud.get_users(pagination)


async def update_user(user_id: UUID, new_user: BaseUser) -> User:
    """
    Service function to update user information.
    """
    try:
        updated_user_cursor = crud.update_user(user_id=user_id, new_user=new_user)
    except Exception as e:
        error_str = f"Failed to update User, user_id={user_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))

    if updated_user_cursor:
        logger.info(f"Updated user, user_id={user_id}, new_user={new_user}")
        return User(userId=user_id, username=new_user.username, email=new_user.email)
    raise HTTPException(*USER_NOT_FOUND)


async def delete_user(user_id: UUID) -> UUID:
    """
    Service function to delete a user by ID.
    """
    existing_user = await get_user(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        crud.delete_user(user_id=user_id)
    except Exception as e:
        error_str = f"Failed to delete User, user_id={user_id}, error={e}"
        logger.error(error_str)
        raise HTTPException(status_code=500, detail=str(e))
    return user_id