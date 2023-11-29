from typing import Optional

from pydantic import UUID4
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import AsyncCRUDBase
from app.models import Series
from app.schemas import SeriesCreate, SeriesFilterAdmin, SeriesUpdate


class AsyncCRUDSeries(AsyncCRUDBase[Series, SeriesCreate, SeriesUpdate]):
    async def _get_filters(
        self,
        series_filter: SeriesFilterAdmin
    ) -> list:
        filters = []
        if series_filter.title is not None:
            filters.append(
                self.model.title.ilike(f"%{series_filter.title}%")
            )
        if series_filter.created_at_start is not None:
            filters.append(
                self.model.created_at >= series_filter.created_at_start
            )
        if series_filter.created_at_end is not None:
            filters.append(
                self.model.created_at <= series_filter.created_at_end
            )
        return filters

    async def get_by_title_and_user(
        self,
        db: AsyncSession,
        *,
        user_uuid: UUID4,
        title: str
    ) -> list[str]:
        q = (
            select(self.model).
            where(and_(
                self.model.user_uuid == user_uuid,
                self.model.title == title
            ))
        )
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: SeriesCreate,
        user_uuid: UUID4
    ) -> Series:
        db_obj = Series(
            **obj_in.model_dump(exclude_none=True),
            user_uuid=user_uuid
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid: UUID4
    ) -> Series:
        q = select(self.model).where(self.model.uuid == uuid).options(
            joinedload(self.model.user)
        )
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 30,
        filters: Optional[str] = None
    ) -> list[Series]:
        q = select(self.model).options(joinedload(self.model.user))
        if filters is not None:
            q = q.where(*await self._get_filters(filters))
        q = (
            q.
            offset(skip).
            limit(limit).
            order_by(self.model.created_at.desc())
        )

        obj = await db.execute(q)
        return obj.scalars()

async_series = AsyncCRUDSeries(Series)
