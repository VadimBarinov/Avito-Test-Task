import datetime
import uuid
from enum import Enum

from pydantic import BaseModel


class EnumCity(str, Enum):
    moscow = "Москва"
    saint_petersburg = "Санкт-Петербург"
    kazan = "Казань"


class PvzBase(BaseModel):
    city: EnumCity


class PvzCreate(PvzBase):
    pass


class PvzRead(PvzBase):
    id: uuid.UUID
    registration_date: datetime.date