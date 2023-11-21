from pydantic import UUID4
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import AsyncCRUDBase
from app.models import Series
from app.schemas import SeriesCreate, SeriesUpdate


class AsyncCRUDSeries(AsyncCRUDBase[Series, SeriesCreate, SeriesUpdate]):
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

async_series = AsyncCRUDSeries(Series)
