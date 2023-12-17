from typing import List
from sqlalchemy.orm import Session
from app.user.models import User, UserCreate
from app.database.database import engine


async def create_user(user: UserCreate) -> User:
    """
    Create a new user using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def get_user(user_id: int) -> User:
    """
    Retrieve a user by ID using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieve a list of users with optional pagination using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def update_user(user_id: int, user: User) -> User:
    """
    Update user information using one of crud operations.
    """
    with Session(engine) as session:
        pass


async def delete_user(user_id: int) -> int:
    """
    Delete a user by ID using one of crud operations.
    """
    with Session(engine) as session:
        pass
