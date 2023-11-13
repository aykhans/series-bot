from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api.deps import get_async_db, get_current_active_superuser
from app.crud import async_crud_user
from app.exceptions import UserAlreadyExistsException, UserNotFoundException

router = APIRouter()


@router.post('/create')
async def create_user(
    user_in: schemas.UserCreate,
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
    user_uuid: UUID4,
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.UserExtended:

    user = await async_crud_user.get_by_uuid(db, uuid=user_uuid)
    if user is None:
        raise UserNotFoundException(detail=f"User not found: {user_uuid}")

    return user


@router.delete('/delete/{user_uuid}')
async def delete_user(
    user_uuid: UUID4,
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db),
) -> dict[str, str]:

    user = await async_crud_user.get_by_uuid(db, uuid=user_uuid)
    if user is None:
        raise UserNotFoundException(detail=f"User not found: {user_uuid}")

    user = await async_crud_user.remove_by_uuid(db, uuid=user_uuid)

    return {'detail': f'User deleted: {user.username}'}


@router.patch('/update/{user_uuid}')
async def update_user(
    user_uuid: UUID4,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db),
) -> schemas.UserExtended:

    user = await async_crud_user.get_by_uuid(db, uuid=user_uuid)
    if user is None:
        raise UserNotFoundException(detail=f"User not found: {user_uuid}")

    user = await async_crud_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.get('/all')
async def get_all_users(
    current_user: models.User = Depends(get_current_active_superuser),
    pagination: schemas.UserPagination = Depends(),
    user_filter: schemas.UserFilter = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.UserList:
    users = async_crud_user.get_multi(
        db,
        skip=pagination.skip,
        limit=pagination.page_size,
        filters=user_filter
    )
    count = async_crud_user.get_count(db, filters=user_filter)

    return schemas.UserList(
        users=await users,
        pagination=schemas.Pagination(total=await count)
    )
