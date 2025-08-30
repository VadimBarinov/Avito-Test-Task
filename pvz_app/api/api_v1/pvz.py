from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper

router = APIRouter(tags=["pvz", ])


@router.post("", summary="Создание ПВЗ (только для модераторов)")
async def create_pvz(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    pass