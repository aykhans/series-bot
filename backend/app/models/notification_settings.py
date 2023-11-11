from sqlalchemy import UUID, Boolean, Column, ForeignKey

from app.db.base_class import Base


class NotificationSettings(Base):
    user_uuid = Column(
        UUID,
        ForeignKey("user.uuid", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    send_email = Column(Boolean(), default=False)
    auto_update = Column(Boolean(), default=False)
