from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params as PaginationParams
from sqlalchemy.orm import Session

from app.api.user import service
from app.api.user.models import BaseUser, User, UserCreate
from app.database.database import get_db

router = APIRouter(prefix="", tags=["User Management"])


@router.post("/users/", response_model=User)
async def create_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> User:
    return await service.create_user(user, db)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: UUID, db: Annotated[Session, Depends(get_db)]) -> User:
    return await service.get_user(user_id, db)


@router.get("/users/", response_model=Page[User])
async def get_users(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
) -> Page[User]:
    return await service.get_users(pagination, db)


@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: UUID, new_user: BaseUser, db: Annotated[Session, Depends(get_db)]
) -> User:
    return await service.update_user(user_id=user_id, new_user=new_user, db=db)


@router.delete("/users/{user_id}", response_model=UUID)
async def delete_user(user_id: UUID, db: Annotated[Session, Depends(get_db)]) -> UUID:
    return await service.delete_user(user_id, db)
