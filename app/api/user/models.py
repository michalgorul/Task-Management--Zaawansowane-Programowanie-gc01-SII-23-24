import re
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import EmailStr, Field, field_validator
from pydantic.types import SecretStr

from app.api.models import BaseModel
from app.api.task.models import Task, TaskWithoutUser


class BaseUser(BaseModel):
    username: str = Field(..., min_length=6, max_length=30)
    email: EmailStr = Field(...)


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=6, max_length=30)
    email: EmailStr | None = Field(None)


class UserResponse(BaseUser):
    user_id: UUID = Field(..., alias="userId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class User(UserResponse):
    tasks: List[Task] | None = Field(None)


class UserTasks(BaseModel):
    user_id: UUID = Field(..., alias="userId")
    tasks: List[TaskWithoutUser] = Field([])


class UserCreate(BaseUser):
    username: str = Field(..., min_length=6, max_length=30)
    email: EmailStr = Field(...)
    password: SecretStr = Field(..., min_length=6, max_length=30)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:
        if not any(char.isdigit() for char in value.get_secret_value()):
            raise ValueError("password must contain at least one digit")

        special_characters = re.compile(r"[!@#$%^&*(),.?\":{}|<>]")
        if not any(
            special_characters.search(char) for char in value.get_secret_value()
        ):
            raise ValueError("password must contain at least one special character")

        return value
