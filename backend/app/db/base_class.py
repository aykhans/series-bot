
import uuid

from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    __name__: str

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=False),
        onupdate=func.now()
    )

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
