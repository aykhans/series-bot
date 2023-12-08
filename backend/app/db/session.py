from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine: Engine = create_engine(
    str(settings.POSTGRES.get_postgres_dsn()),
    pool_pre_ping=True
)

SessionLocal: Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


async_engine: AsyncEngine = create_async_engine(
    str(settings.POSTGRES.get_postgres_dsn(_async=True)),
    future=True
)

AsyncSessionLocal: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)
