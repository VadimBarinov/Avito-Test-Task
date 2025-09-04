from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.pvz import PvzCreate, PvzRead


async def create_new_pvz(
        session: AsyncSession,
        pvz_data: PvzCreate,
) -> PvzRead:
    pass