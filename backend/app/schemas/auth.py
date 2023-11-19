from typing import Annotated

from pydantic import BaseModel, Field

AccessToken = Annotated[
    str,
    Field()
]
TokenType = Annotated[
    str,
    Field()
]
Sub = Annotated[
    str,
    Field(
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}"\
            r"-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}"\
                r"-[0-9a-fA-F]{12}\$\b(true|false)\b\$\b(true|false)\b$"
    ) # pattern: uuid$is_active$is_superuser
]


class JWTToken(BaseModel):
    access_token: AccessToken
    token_type: TokenType


class JWTPayload(BaseModel):
    sub: Sub

    @property
    def uuid(self):
        return self.sub.split('$')[0]

    @property
    def is_active(self):
        if self.sub.split('$')[1] == 'true':
            return True
        return False

    @property
    def is_superuser(self):
        if self.sub.split('$')[2] == 'true':
            return True
        return False
