import uuid
from typing import Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.helpers import (
    SUB_TYPE_FIELD,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE, DUMMY_LOGIN_TYPE, ROLE_TYPE_FIELD,
)
from auth.utils import decode_jwt
from core.db_helper import db_helper
from core.schemas.auth import RoleEnum
from core.schemas.users import UserRead
from crud.users import UserCRUD

http_bearer = HTTPBearer()


def get_current_token_payload(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]
) -> dict:
    try:
        token = credentials.credentials
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не валидный!"
        )
    return payload


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный тип токена!"
    )


async def get_user_by_token_payload(
        session: AsyncSession,
        payload: dict,
) -> UserRead:
    user_id = payload.get(SUB_TYPE_FIELD)
    user = await UserCRUD.get_by_id(
        session=session,
        user_id=uuid.UUID(user_id),
    )
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не валидный!"
    )


def get_role_by_token_payload(
        payload: dict,
) -> RoleEnum:
    return payload.get(ROLE_TYPE_FIELD)


class GetterRoleFromPayload:
    def __init__(
            self,
            token_type: str,
    ):
        self.token_type = token_type

    async def __call__(
            self,
            session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
            payload: Annotated[dict, Depends(get_current_token_payload)],
    ):
        sub = payload.get(SUB_TYPE_FIELD)
        if sub != DUMMY_LOGIN_TYPE:
            await get_user_by_token_payload(
                session=session,
                payload=payload,
            )
        return get_role_by_token_payload(payload=payload)


def get_current_auth_user_is_moderator(
        role: Annotated[RoleEnum, Depends(GetterRoleFromPayload(token_type=ACCESS_TOKEN_TYPE))]
) -> bool:
    if role == RoleEnum.moderator:
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещен"
    )

