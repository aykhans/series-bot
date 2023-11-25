from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.config import settings
from app.crud import async_crud_user
from app.db.session import AsyncSessionLocal, SessionLocal
from app.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    NotSuperuserException,
    UserNotFoundException,
)
from app.schemas import JWTPayload

admin_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/{settings.ADMIN_STR}/login"
)


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


async def get_async_db() -> Generator:
    async with AsyncSessionLocal() as async_db:
        yield async_db


async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    token: str = Depends(admin_oauth2)
) -> models.User:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = JWTPayload(**payload)

    except (jwt.JWTError, ValidationError) as exc:
        raise InvalidCredentialsException() from exc

    user = await async_crud_user.get_by_uuid(db, uuid=token_data.uuid)
    if user is None:
        raise UserNotFoundException()

    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:

    if current_user.is_active is False:
        raise InactiveUserException()

    return current_user

async def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:

    if current_user.is_superuser is False:
        raise NotSuperuserException()

    return current_user