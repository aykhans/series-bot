from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.security import create_jwt_access_token
from app.crud import async_crud_user
from app.exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    NotSuperuserException,
)
from app.schemas import JWTToken
from app.utils import jwt

router = APIRouter()


@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> JWTToken:

    user = await async_crud_user.authenticate(
        db,
        username=form_data.username,
        password=form_data.password
    )

    if user is None:
        raise InvalidCredentialsException()

    elif user.is_active is False:
        raise InactiveUserException()

    elif user.is_superuser is False:
        raise NotSuperuserException(detail='Not a superuser')

    return JWTToken(
        access_token=await create_jwt_access_token(
            subject=await jwt.create_sub(
                uuid=str(user.uuid),
                is_active=True,
                is_superuser=True
            )
        ),
        token_type="bearer"
    )
