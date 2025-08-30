from fastapi import APIRouter

from core.config import settings
from .auth import router as auth_router
from .pvz import router as pvz_router


router = APIRouter()

router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)
router.include_router(
    pvz_router,
    prefix=settings.api.v1.pvz,
)