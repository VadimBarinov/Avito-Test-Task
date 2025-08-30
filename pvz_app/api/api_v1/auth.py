from fastapi import (
    APIRouter,
)

from core.schemas.auth import DummyLogin

router = APIRouter(tags=["auth"])


@router.post("/dummy-login", summary="Получение тестового токена", response_model=dict)
def dummy_login(data: DummyLogin):
    return {
        "role": data.role,
    }
