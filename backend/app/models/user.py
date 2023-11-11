from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models import NotificationSettings


class User(Base):
    username = Column(String(35), index=True, nullable=False, unique=True)
    email = Column(String(320), unique=True, index=True, nullable=True)
    hashed_password = Column(String(72), nullable=False)
    is_email_verified = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    notification_settings = relationship(
        'NotificationSettings',
        backref="user",
        uselist=False,
        passive_deletes=True,
        cascade='all,delete'
    )
    series = relationship(
        'Series',
        backref="user"
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.notification_settings = NotificationSettings()
