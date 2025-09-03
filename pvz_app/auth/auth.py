import uuid

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from core.schemas.users import UserCreate, UserRead, UserBase
from crud.users import UserCRUD


async def create_new_user(
        session: AsyncSession,
        user: UserCreate,
) -> UserRead:
    found_user = await UserCRUD.get_user_by_email(
        session=session,
        email=user.email,
    )
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует!"
        )
    user_result = user.copy()
    user_result.password = hash_password(user_result.password).decode()
    added_user_result = await UserCRUD.user_create(
        session=session,
        user=user_result,
    )
    if added_user_result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь не зарегистрирован!"
        )
    return added_user_result


async def get_user(
        session: AsyncSession,
        user_id: uuid.UUID,
) -> UserRead:
    found_user = await UserCRUD.get_by_id(
        session=session,
        user_id=user_id,
    )
    return found_user


async def validate_auth_user(
        session: AsyncSession,
        user: UserBase,
) -> bool:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные!"
    )
    found_user = UserCRUD.get_user_by_email()
