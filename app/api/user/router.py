from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params as PaginationParams

from app.api.user import service
from app.api.user.models import UserCreate, User, BaseUser

router = APIRouter(prefix="", tags=["User Management"])


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate) -> User:
    return await service.create_user(user)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID) -> User:
    return await service.get_user(user_id)


@router.get("/users/", response_model=Page[User])
async def get_users(pagination: PaginationParams = Depends()) -> Page[User]:
    return await service.get_users(pagination)


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, new_user: BaseUser) -> User:
    return await service.update_user(user_id=user_id, new_user=new_user)


@router.delete("/users/{user_id}", response_model=UUID)
async def delete_user(user_id: UUID) -> UUID:
    return await service.delete_user(user_id)
