import uuid
from datetime import timedelta, timezone, datetime

import bcrypt
import jwt

from core.config import settings

auth_data = settings.auth_jwt


def encode_jwt(
        payload: dict,
        private_key: str = auth_data.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = auth_data.ALGORITHM,
        expire_timedelta: timedelta = 0,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expires_in = now + expire_timedelta
    to_encode.update(
        exp=expires_in,
        iat=now,
        jti=str(uuid.uuid4())
    )
    return jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )


def decode_jwt(
        token: str | bytes,
        public_key: str = auth_data.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = auth_data.ALGORITHM,
) -> dict:
    return jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=algorithm,
    )


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        password=password.encode(),
        salt=salt,
    )


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )