from fastapi import APIRouter

from app.api.v1.endpoints.admin import login, user
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(
    login.router,
    prefix=f"/{settings.ADMIN_STR}",
    tags=['admin'],
    include_in_schema=settings.DEBUG
)
api_router.include_router(
    user.router,
    prefix=f"/{settings.ADMIN_STR}/user",
    tags=['admin'],
    include_in_schema=settings.DEBUG
)
