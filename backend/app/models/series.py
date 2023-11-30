from sqlalchemy import UUID, Column, ForeignKey, SmallInteger, String, UniqueConstraint

from app.db.base_class import Base


class Series(Base):
    user_uuid = Column(
        UUID,
        ForeignKey("user.uuid", ondelete="CASCADE"),
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

    __table_args__ = (
        UniqueConstraint('user_uuid', 'title', name='uq_user_title'),
    )
