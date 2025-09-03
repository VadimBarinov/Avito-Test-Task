import uuid

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    table = None