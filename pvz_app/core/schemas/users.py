import uuid

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)\


class UserCreate(UserBase):
    is_employee: bool = Field(False)
    is_moderator: bool = Field(False)


class UserRead(UserCreate):
    id: uuid.UUID
