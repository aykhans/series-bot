from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


class AsyncCRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methodts to Create, Read, Update, Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def _get_filters(
        self,
        filters: FilterSchemaType
    ) -> list:
        raise NotImplementedError(
            f"Method `_get_filters`"\
                f"not implemented for `{self.__class__.__name__}`"
        )

    async def get_by_uuid(
        self,
        db: AsyncSession,
        uuid: str
    ) -> Optional[ModelType]:
        q = select(self.model).where(self.model.uuid == uuid)
        obj = await db.execute(q)
        return obj.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[FilterSchemaType] = None
    ) -> list[ModelType]:
        q = select(self.model)
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

    async def get_count(
        self, db: AsyncSession, *, filters: Optional[FilterSchemaType] = None
    ) -> int:
        q = select(func.count(self.model.uuid))
        if filters is not None:
            q = q.where(*await self._get_filters(filters))
        obj = await db.execute(q)
        return obj.scalar_one()

    async def create(
        self, db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        from pprint import pprint
        obj_in_data = jsonable_encoder(obj_in)
        pprint(obj_in_data)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def remove_by_uuid(
        self,
        db: AsyncSession,
        *,
        uuid: str
    ) -> ModelType:
        q = select(self.model).where(self.model.uuid == uuid)
        obj = await db.execute(q)
        obj = obj.scalar_one()
        await db.delete(obj)
        await db.commit()

        return obj


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methodts to Create, Read, Update, Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_by_uuid(self, db: Session, uuid: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()
