
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from app.core.security import (
    get_password_hash,
    get_password_hash_sync,
    verify_password,
)
from app.crud import async_crud_notification_settings
from app.crud.base import AsyncCRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class AsyncCRUDUser(AsyncCRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=await get_password_hash(obj_in.password),
            username=obj_in.username,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: UserUpdate
    ) -> User:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = await get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        if obj_in.notification_settings is not None:
            await async_crud_notification_settings.update(
                db,
                db_obj=db_obj.notification_settings,
                obj_in=obj_in.notification_settings
            )
            del update_data["notification_settings"]

        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid: str
    ) -> User:
        q = select(self.model).where(self.model.uuid == uuid).options(
            joinedload(self.model.notification_settings)
        )
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_by_username(
        self,
        db: AsyncSession,
        *,
        username: str
    ) -> User:
        q = select(self.model).where(self.model.username.ilike(username))
        obj = await db.execute(q)

        return obj.scalar_one_or_none()

    async def get_by_email(
        self,
        db: AsyncSession,
        *,
        email: str
    ) -> User:
        q = select(self.model).where(self.model.email.ilike(email))
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_by_username_or_email(
        self,
        db: AsyncSession,
        *,
        username_or_email: str
    ) -> User:
        q = select(self.model).where(
            (self.model.username.ilike(username_or_email)) |
            (self.model.email.ilike(username_or_email))
        )
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def authenticate(
        self,
        db: AsyncSession,
        *,
        username: str,
        password: str
    ) -> User:
        user = await self.get_by_username_or_email(
            db,
            username_or_email=username
        )

        if user is None:
            return None

        if await verify_password(password, user.hashed_password) is False:
            return None

        return user

async_user = AsyncCRUDUser(User)


class CRUDUser(AsyncCRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash_sync(obj_in.password),
            username=obj_in.username,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_username(
        self,
        db: Session,
        *,
        username: str
    ) -> User:
        return db.query(self.model).filter(
            self.model.username.ilike(username)
        ).first()

    def get_by_email(
        self,
        db: Session,
        *,
        email: str
    ) -> User:
        return db.query(self.model).filter(
            self.model.email.ilike(email)
        ).first()

user = CRUDUser(User)
