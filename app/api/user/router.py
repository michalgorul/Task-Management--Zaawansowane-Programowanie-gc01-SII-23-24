from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params as PaginationParams
from sqlalchemy.orm import Session

from app.api.user import service
from app.api.user.models import User, UserCreate, UserResponse, UserTasks, UserUpdate
from app.database.database import get_db

router = APIRouter(prefix="/users", tags=["User Management"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    return await service.create_user(user, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID, db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    return await service.get_user(user_id, db)


@router.get("/tasks/{user_id}", response_model=UserTasks)
async def get_user_tasks(
    user_id: UUID, db: Annotated[Session, Depends(get_db)]
) -> UserTasks:
    return await service.get_user_tasks(user_id, db)


@router.get("/", response_model=Page[UserResponse])
async def get_users(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
) -> Page[UserResponse]:
    return await service.get_users(pagination, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID, new_user: UserUpdate, db: Annotated[Session, Depends(get_db)]
) -> UserResponse:
    return await service.update_user(user_id=user_id, new_user=new_user, db=db)


@router.delete("/{user_id}", response_model=UUID)
async def delete_user(user_id: UUID, db: Annotated[Session, Depends(get_db)]) -> UUID:
    return await service.delete_user(user_id, db)
