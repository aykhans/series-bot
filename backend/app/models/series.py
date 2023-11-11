from sqlalchemy import UUID, Column, ForeignKey, SmallInteger, String

from app.db.base_class import Base


class Series(Base):
    user_uuid = Column(
        UUID,
        ForeignKey("user.uuid"),
        nullable=False
    )
    title = Column(String(255), nullable=False)
    watched_season = Column(SmallInteger(), nullable=False)
    watched_episode = Column(SmallInteger(), nullable=False)
    last_season = Column(SmallInteger(), nullable=False)
    last_episode = Column(SmallInteger(), nullable=False)
    unwatched_episodes_count = Column(
        SmallInteger(),
        nullable=False,
        default=0
    )
