from typing import Annotated

from pydantic import UUID4 as PydanticUUID4
from pydantic import Field, PastDatetime

UUID4 = Annotated[
    PydanticUUID4,
    Field(
        description='UUID version 4',
        example='123e4567-e89b-12d3-a456-426614174000'
    )
]
CreatedAt = Annotated[
    PastDatetime,
    Field(
        description='Datetime when the object was created',
        example='2020-01-01T00:00:00'
    )
]
UpdatedAt = Annotated[
    PastDatetime,
    Field(
        description='Datetime when the object was updated',
        example='2020-01-01T00:00:00'
    )
]
