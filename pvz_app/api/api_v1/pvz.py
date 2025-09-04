from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth.validation import get_current_auth_user_is_moderator
from core.db_helper import db_helper
from core.schemas.pvz import PvzCreate
from pvz.utils import create_new_pvz

router = APIRouter(tags=["pvz", ])


@router.post("/", summary="Создание ПВЗ (только для модераторов)", response_model=dict)
async def create_pvz(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        is_moderator: Annotated[bool, Depends(get_current_auth_user_is_moderator)],
        pvz_data: Annotated[PvzCreate, Depends()],
):
    created_pvz = await create_new_pvz(
        session=session,
        pvz_data=pvz_data,
    )
    return {
        "message": "ПВЗ создан!",
        "pvz": created_pvz,
    }