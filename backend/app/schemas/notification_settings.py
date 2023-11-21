from typing import Annotated, Optional

from pydantic import BaseModel, Field

SendEmail = Annotated[
    bool,
    Field(default=False)
]
AutoUpdate = Annotated[
    bool,
    Field(default=False)
]


class NotificationSettingsBase(BaseModel):
    send_email: Optional[SendEmail] = False
    auto_update: Optional[AutoUpdate] = False


class NotificationSettingsCreate(NotificationSettingsBase):
    pass


class NotificationSettingsUpdate(NotificationSettingsBase):
    pass


class NotificationSettings(NotificationSettingsBase):
    class Config:
        from_attributes = True
