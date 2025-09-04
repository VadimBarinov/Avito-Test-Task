import uuid

from pydantic import EmailStr
from sqlalchemy import Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.schemas.users import UserCreate, UserRead
from core.tables_names import USERS_TABLE_NAME
from crud.base import BaseCRUD


class UserCRUD(BaseCRUD):
    table = USERS_TABLE_NAME

    @classmethod
    async def get_user_by_email(
            cls,
            session: AsyncSession,
            email: EmailStr
    ) -> UserRead | None:
        stmt = text("""
            SELECT * FROM %s WHERE email = :email;
        """ % (cls.table, )).bindparams(email=email)
        result = await session.execute(stmt)
        found_user = result.first()
        if not found_user:
            return None
        return UserRead(
            id=found_user.id,
            email=found_user.email,
            password=found_user.password,
            is_employee=found_user.is_employee,
            is_moderator=found_user.is_moderator,
        )

    @classmethod
    async def user_create(
            cls,
            session: AsyncSession,
            user: UserCreate,
    ) -> UserRead:
        stmt = text("""
            INSERT INTO %s (
                email,
                password,
                is_employee,
                is_moderator
            ) VALUES (
                :email,
                :password,
                :is_employee,
                :is_moderator
            ) RETURNING *;
        """ % (cls.table,)).bindparams(**user.model_dump())
        result = await session.execute(stmt)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        created_user = result.first()
        return UserRead(
            id=created_user.id,
            email=created_user.email,
            password=created_user.password,
            is_employee=created_user.is_employee,
            is_moderator=created_user.is_moderator,
        )