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

from auth.helpers import SUB_TYPE_FIELD
from auth.utils import decode_jwt
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

