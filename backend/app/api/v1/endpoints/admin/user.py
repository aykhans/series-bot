from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api.deps import (
    get_async_db,
    get_current_active_superuser,
    get_user_by_uuid,
)
from app.crud import async_crud_user
from app.exceptions import UserAlreadyExistsException

router = APIRouter()


@router.post('/create')
async def create_user(
    user_in: schemas.UserCreateAdmin,
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.User:
    user = await async_crud_user.get_by_username(
        db, username=user_in.username
    )
    if user is not None:
        raise UserAlreadyExistsException(
            detail=f'This username already exists: {user_in.username}'
        )

    if user_in.email is not None:
        user = await async_crud_user.get_by_email(
            db, email=user_in.email
        )
        if user is not None:
            raise UserAlreadyExistsException(
                detail=f'This email already exists: {user_in.email}'
            )

    user = await async_crud_user.create(
        db,
        obj_in=user_in
    )
    return user


@router.get('/detail/{user_uuid}')
async def get_user(
    current_user: models.User = Depends(get_current_active_superuser),
    user: models.User = Depends(get_user_by_uuid)
) -> schemas.UserExtended:
    return user


@router.delete('/delete/{user_uuid}')
async def delete_user(
    current_user: models.User = Depends(get_current_active_superuser),
    user: models.User = Depends(get_user_by_uuid),
    db: AsyncSession = Depends(get_async_db)
) -> dict[str, str]:
    user = await async_crud_user.remove_by_uuid(db, uuid=user.uuid)
    return {'detail': f'User deleted: {user.username}'}


@router.patch('/update/{user_uuid}')
async def update_user(
    user_in: schemas.UserUpdateAdmin,
    current_user: models.User = Depends(get_current_active_superuser),
    user: models.User = Depends(get_user_by_uuid),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.UserExtended:
    user = await async_crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.get('/all')
async def get_all_users(
    current_user: models.User = Depends(get_current_active_superuser),
    pagination: schemas.UserPagination = Depends(),
    user_filter: schemas.UserFilterAdmin = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.UserListAdmin:
    users = async_crud_user.get_multi(
        db,
        skip=pagination.skip,
        limit=pagination.page_size,
        filters=user_filter
    )
    count = async_crud_user.get_count(db, filters=user_filter)

    return schemas.UserListAdmin(
        users=await users,
        pagination=schemas.Pagination(total=await count, page=pagination.page)
    )


@router.get('/usernames')
async def get_usernames(
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db),
    username: Annotated[str, Query(min_length=1, max_length=35)] = None,
    size: Annotated[int, Query(ge=1, le=100)] = 20
) -> list[schemas.UsernameResponseAdmin]:
    users = await async_crud_user.get_multi(
        db,
        limit=size,
        filters=schemas.UserFilterAdmin(username=username)
    )
    return users


@router.get('/emails', response_model=list[schemas.User])
async def get_emails(
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db),
    email: Annotated[str, Query(min_length=1, max_length=72)] = None,
    size: Annotated[int, Query(ge=1, le=100)] = 20
) -> list[schemas.EmailResponseAdmin]:
    users = await async_crud_user.get_multi(
        db,
        limit=size,
        filters=schemas.UserFilterAdmin(email=email)
    )
    return users


@router.get('/me')
async def get_me(
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.UserExtended:
    return await async_crud_user.get_by_uuid(db, uuid=current_user.uuid)
