from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field, PastDatetime

from app.schemas.notification_settings import (
    NotificationSettings,
    NotificationSettingsUpdate,
)
from app.schemas.pagination import Pagination


class UserBase(BaseModel):
    username: Optional[str] = Field(
        min_length=1,
        max_length=35,
        pattern=r'^[a-zA-Z0-9_-]+$',
        default=None,
        examples=['JohnDoe', 'johndoe0', 'john_doe', 'john-doe']
    )
    email: Optional[EmailStr] = Field(max_length=72, default=None)
    is_email_verified: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: bool = False

# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str = Field(
        min_length=1,
        max_length=35,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    password: str = Field(min_length=8, max_length=72)


# Properties to receive via API on creation
class UserUpdate(UserBase):
    password: Optional[str] = None
    notification_settings: Optional[NotificationSettingsUpdate] = None


class UserCreateCommand(UserCreate):
    username: str = Field(
        min_length=1,
        max_length=35,
        pattern=r'^[a-zA-Z0-9_-]+$',
        default=None
    )
    password: str = Field(min_length=8, max_length=72, default=None)

    class Config:
        validate_assignment = True


class UserInDBBase(UserBase):
    created_at: Optional[PastDatetime] = None
    uuid: Optional[UUID4] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserExtended(UserInDBBase):
    notification_settings: NotificationSettings

class UserList(BaseModel):
    users: list[User]
    pagination: Pagination


class UserFilter(UserBase):
    email: Optional[str] = Field(max_length=72, default=None)
    is_email_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    created_at_start: Optional[PastDatetime] = None
    created_at_end: Optional[PastDatetime] = None
