from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import AsyncCRUDBase
from app.models import NotificationSettings
from app.schemas import NotificationSettingsCreate, NotificationSettingsUpdate


class AsyncCRUDNotificationSettings(
    AsyncCRUDBase[
        NotificationSettings,
        NotificationSettingsCreate,
        NotificationSettingsUpdate
    ]
):
    async def get_by_user_uuid(
        self,
        db: AsyncSession,
        *,
        user_uuid: str
    ) -> Optional[NotificationSettings]:
        q = select(self.model).where(self.model.user_uuid == user_uuid)
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: NotificationSettingsCreate,
        user_uuid: str
    ) -> NotificationSettings:
        db_obj = NotificationSettings(
            **obj_in.model_dump(),
            user_uuid=user_uuid
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

async_notification_settings = \
    AsyncCRUDNotificationSettings(NotificationSettings)
