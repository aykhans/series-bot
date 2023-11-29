from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas import base, pagination
from app.schemas import notification_settings as notification_schemas

# Custom fields
Username = Annotated[
    str,
    Field(
        min_length=1,
        max_length=35,
        pattern=r'^[a-zA-Z0-9_-]+$',
        examples=['JohnDoe', 'johndoe0', 'john_doe', 'john-doe']
    )
]
Email = Annotated[
    EmailStr,
    Field(max_length=72, examples=['john@gmail.com']),
]
Password = Annotated[
    str,
    Field(min_length=8, max_length=72)
]
IsEmailVerified = Annotated[
    bool,
    Field(default=False)
]
IsActive = Annotated[
    bool,
    Field(default=True)
]
IsSuperuser = Annotated[
    bool,
    Field(default=False)
]


class UserCreate(BaseModel):
    username: Username
    password: Password
    email: Optional[Email] = None


class UserCreateAdmin(UserCreate):
    is_email_verified: Optional[IsEmailVerified] = False
    is_active: Optional[IsActive] = True
    is_superuser: Optional[IsSuperuser] = False


class UserCreateCommand(UserCreateAdmin):
    username: Optional[Username] = None
    password: Optional[Password] = None

    class Config:
        validate_assignment = True


class UserUpdate(BaseModel):
    username: Optional[Username] = None
    email: Optional[Email] = None
    password: Optional[Password] = None
    notification_settings: Optional[
        notification_schemas.NotificationSettingsUpdate
    ] = None


class UserUpdateAdmin(UserUpdate):
    is_email_verified: Optional[IsEmailVerified] = None
    is_active: Optional[IsActive] = None
    is_superuser: Optional[IsSuperuser] = None


class User(BaseModel):
    username: Optional[Username] = None
    email: Optional[Email] = None
    is_email_verified: Optional[IsEmailVerified] = False
    is_active: Optional[IsActive] = True
    is_superuser: Optional[IsSuperuser] = False
    created_at: Optional[base.CreatedAt] = None
    uuid: Optional[base.UUID4] = None

    class Config:
        from_attributes = True


class UserExtended(User):
    notification_settings: Optional[
        notification_schemas.NotificationSettings
    ] = None


class UserListAdmin(BaseModel):
    users: list[User]
    pagination: pagination.Pagination


class UserFilterAdmin(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=35)
    email: Optional[str] = Field(None, min_length=1, max_length=72)
    is_email_verified: Optional[IsEmailVerified] = None
    is_active: Optional[IsActive] = None
    is_superuser: Optional[IsSuperuser] = None
    created_at_start: Optional[base.CreatedAt] = None
    created_at_end: Optional[base.CreatedAt] = None


class UsernameResponseAdmin(BaseModel):
    username: Username
    uuid: base.UUID4


class EmailResponseAdmin(BaseModel):
    email: Email
    uuid: base.UUID4

class UserInSeries(BaseModel):
    uuid: base.UUID4
    username: Username
    email: Optional[Email] = None

    class Config:
        from_attributes = True
