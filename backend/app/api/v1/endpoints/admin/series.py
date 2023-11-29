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
    db: AsyncSession = Depends(get_async_db)
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
    series: models.Series = Depends(get_series_by_uuid)
) -> schemas.SeriesUser:
    return series


@router.delete('/delete/{series_uuid}')
async def delete_series(
    current_user: models.User = Depends(get_current_active_superuser),
    series: models.Series = Depends(get_series_by_uuid),
    db: AsyncSession = Depends(get_async_db)
) -> dict[str, str]:
    await async_crud_series.remove_by_uuid(db, uuid=series.uuid)
    return {'detail': f'Series deleted: {series.title}'}


@router.patch('/update/{series_uuid}', response_model_exclude={'created_at'})
async def update_series(
    series_in: schemas.SeriesUpdateAdmin,
    current_user: models.User = Depends(get_current_active_superuser),
    series: models.Series = Depends(get_series_by_uuid),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.Series:
    if series_in.title is not None and series_in.title != series.title:
        series_db = await async_crud_series.get_by_title_and_user(
            db,
            user_uuid=series.user_uuid,
            title=series_in.title
        )
        if series_db is not None:
            raise SeriesAlreadyExistsException(
                detail="This user already has "
                    f"series with title `{series_in.title}`"
            )

    series = await async_crud_series.update(
        db,
        db_obj=series,
        obj_in=series_in
    )
    return series


@router.get('/all')
async def get_all_series(
    current_user: models.User = Depends(get_current_active_superuser),
    pagination: schemas.SeriesPagination = Depends(),
    series_filter: schemas.SeriesFilterAdmin = Depends(),
    db: AsyncSession = Depends(get_async_db)
) -> schemas.SeriesListAdmin:
    series = await async_crud_series.get_multi(
        db,
        skip=pagination.skip,
        limit=pagination.page_size,
        filters=series_filter
    )
    count = await async_crud_series.get_count(
        db,
        filters=series_filter
    )

    return schemas.SeriesListAdmin(
        series=series,
        pagination=schemas.Pagination(total=count, page=pagination.page)
    )
