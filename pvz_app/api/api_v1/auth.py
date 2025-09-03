import uuid

from fastapi import (
    APIRouter,
)

from auth.helpers import create_access_token
from core.schemas.auth import DummyLogin


router = APIRouter(tags=["auth"])


@router.post("/dummy-login", summary="Получение тестового токена", response_model=dict)
def dummy_login(data: DummyLogin):
    token = create_access_token(
        user_id=str(uuid.uuid4()),
        role=data.role,
    )
    return {
        "role": data.role,
        "access_token": token,
    }

