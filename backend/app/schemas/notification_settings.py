from typing import Optional

from pydantic import UUID4, BaseModel

# API Schemas

class NotificationSettingsBase(BaseModel):
    send_email: Optional[bool] = False
    auto_update: Optional[bool] = False

class NotificationSettingsCreate(NotificationSettingsBase):
    pass

class NotificationSettingsUpdate(NotificationSettingsBase):
    pass

# In DB Schemas

class NotificationSettingsInDBBase(NotificationSettingsBase):
    user_uuid: Optional[UUID4] = None

    class Config:
        from_attributes = True

class NotificationSettings(NotificationSettingsBase):
    pass

class NotificationSettingsInDB(NotificationSettingsBase):
    user_uuid: Optional[UUID4]
