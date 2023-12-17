from typing import List

from fastapi import APIRouter

from app.user.models import UserCreate, User

router = APIRouter(prefix="", tags=["User Management"])


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate) -> User:
    pass


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    pass


@router.get("/users/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100) -> List[User]:
    pass


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User) -> User:
    pass


@router.delete("/users/{user_id}", response_model=int)
async def delete_user(user_id: int) -> int:
    pass
