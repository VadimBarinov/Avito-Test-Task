from enum import Enum

from pydantic import BaseModel

class RoleEnum(str, Enum):
    employee = "employee"
    moderator = "moderator"

class DummyLogin(BaseModel):
    role: RoleEnum