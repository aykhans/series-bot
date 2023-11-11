from pydantic import BaseModel, Field


class JWTToken(BaseModel):
    access_token: str
    token_type: str

class JWTPayload(BaseModel):
    sub: str = Field(
        pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB]"\
            r"[0-9a-fA-F]{3}-[0-9a-fA-F]{12}\$\b(true|false)\b\$\b(true|false)\b$"
    ) # pattern: uuid$is_active$is_superuser

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
