from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import create_new_user, validate_auth_user, get_user_role
from auth.helpers import create_access_token
from core.db_helper import db_helper
from core.schemas.auth import DummyLogin, TokenInfo
from core.schemas.users import UserRead, UserCreate, UserBase


router = APIRouter(tags=["auth"])


@router.post("/dummy-login/", summary="Получение тестового токена", response_model=dict)
def dummy_login(data: Annotated[DummyLogin, Depends()]):
    token = create_access_token(role=data.role)
    return {
        "role": data.role,
        "access_token": token,
    }


@router.post("/register/", summary="Регистрация нового пользователя", response_model=dict)
async def register_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: Annotated[UserCreate, Depends()],
):
    created_user = await create_new_user(session=session, user=user)
    return {
        "message": "Пользователь зарегистрирован!",
        "user_id": created_user,
    }


@router.post("/login/", summary="Авторизация пользователя", response_model=TokenInfo)
async def login_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user: Annotated[UserBase, Depends()],
):
    found_user = await validate_auth_user(session=session, user=user)
    access_token = create_access_token(
        user_id=str(found_user.id),
        role=get_user_role(found_user),
    )
    return TokenInfo(
        access_token=access_token,
    )



