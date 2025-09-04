from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.schemas.pvz import PvzCreate, PvzRead
from core.tables_names import PVZ_TABLE_NAME
from crud.base import BaseCRUD


class PvzCRUD(BaseCRUD):
    table = PVZ_TABLE_NAME

    @classmethod
    async def pvz_create(
            cls,
            session: AsyncSession,
            pvz_data: PvzCreate,
    ) -> PvzRead:
        stmt = text("""
            INSERT INTO %s (city) VALUES (:city) RETURNING *;
        """ % (cls.table, )).bindparams(**pvz_data)
        result = await session.execute(stmt)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        created_pvz = result.first()
        return PvzRead(
            id=created_pvz.id,
            city=created_pvz.city,
            registration_date=created_pvz.registration_date,
        )