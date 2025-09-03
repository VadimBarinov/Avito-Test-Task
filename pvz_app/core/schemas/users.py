import uuid

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)
    is_employee: bool = Field(False)
    is_moderator: bool = Field(False)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID