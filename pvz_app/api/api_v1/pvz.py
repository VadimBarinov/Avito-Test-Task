from typing import Annotated

from fastapi import (
    APIRouter,
    Depends
)

from auth.validation import get_current_auth_user_is_moderator

router = APIRouter(tags=["pvz", ])


@router.post("/", summary="Создание ПВЗ (только для модераторов)")
async def create_pvz(is_moderator: Annotated[bool, Depends(get_current_auth_user_is_moderator)]):
    pass