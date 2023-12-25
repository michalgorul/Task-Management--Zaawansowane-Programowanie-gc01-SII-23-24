from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.api.models import BaseModel


class BaseTask(BaseModel):
    name: str = Field(..., min_length=3, max_length=36)
    description: str = Field(..., max_length=256)

    user_id: UUID = Field(..., alias="userId")


class TaskUpdate(BaseModel):
    name: str | None = Field(None, max_length=36)
    description: str | None = Field(None, max_length=256)


class TaskCreate(BaseTask):
    pass


class Task(BaseTask):
    task_id: UUID = Field(..., alias="taskId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class TaskWithoutUser(BaseModel):
    name: str = Field(..., min_length=3, max_length=36)
    description: str = Field(..., max_length=256)
    task_id: UUID = Field(..., alias="taskId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")
