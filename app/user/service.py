from typing import List
from app.user.models import User, UserCreate


async def create_user(user: UserCreate) -> User:
    """
    Service function to create a new user.
    """
    pass


async def get_user(user_id: int) -> User:
    """
    Service function to retrieve a user by ID.
    """
    pass


async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    """
    Service function to retrieve a list of users with optional pagination.
    """
    pass


async def update_user(user_id: int, user: User) -> User:
    """
    Service function to update user information.
    """
    pass


async def delete_user(user_id: int) -> int:
    """
    Service function to delete a user by ID.
    """
    pass
