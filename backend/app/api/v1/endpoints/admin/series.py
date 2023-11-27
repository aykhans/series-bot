from typing import Annotated

from fastapi import APIRouter, Body, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api.deps import (
    get_async_db,
    get_current_active_superuser,
    get_series_by_uuid,
)
from app.crud import async_crud_series, async_crud_user
from app.exceptions import (
    SeriesAlreadyExistsException,
    UserNotExistsException,
)

router = APIRouter()


@router.post('/create')
async def create_series(
    series: schemas.SeriesCreate,
    user_uuid: Annotated[UUID4, Body()],
    current_user: models.User = Depends(get_current_active_superuser),
    db: AsyncSession = Depends(get_async_db),
) -> schemas.Series:
    series_db = await async_crud_series.get_by_title_and_user(
        db, user_uuid=user_uuid, title=series.title
    )
    if series_db is not None:
        raise SeriesAlreadyExistsException(
            detail=f"This user already has series with title `{series.title}`"
        )

    user = await async_crud_user.get_by_uuid(db, uuid=user_uuid)
    if user is None:
        raise UserNotExistsException(
            detail=f"User with uuid `{user_uuid}` not found"
        )

    series_db = await async_crud_series.create(
        db,
        obj_in=series,
        user_uuid=user_uuid
    )
    return series_db


@router.get('/detail/{series_uuid}')
async def get_series(
    current_user: models.User = Depends(get_current_active_superuser),
    series: models.Series = Depends(get_series_by_uuid),
) -> schemas.SeriesExtended:
    return series
