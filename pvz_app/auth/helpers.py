from datetime import timedelta

from auth.utils import encode_jwt
from core.config import settings
from core.schemas.auth import RoleEnum

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_timedelta: timedelta | None = None,
) -> str:
    payload = {
        TOKEN_TYPE_FIELD: token_type,
    }
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(
        user_id: str,
        role: RoleEnum = RoleEnum.employee,
) -> str:
    payload = {
        "sub": user_id,
        "role": role,
    }
    expire_timedelta = timedelta(minutes=settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=expire_timedelta
    )