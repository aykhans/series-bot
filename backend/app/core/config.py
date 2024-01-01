from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class CORSSettings(BaseSettings):
    ALLOW_ORIGINS: list = ['*']
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']


class Postgres(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    def get_postgres_dsn(self, _async: bool = False) -> PostgresDsn:
        scheme = 'postgresql+asyncpg' if _async else 'postgresql'

        return PostgresDsn.build(
            scheme=scheme,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        )


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Series Robot V2'

    SECRET_KEY: str
    DEBUG: bool = True

    CORS: CORSSettings = CORSSettings()

    MAIN_PATH: Path = Path(__file__).resolve().parent.parent.parent
    APP_PATH: Path = Path(__file__).resolve().parent.parent

    API_V1_STR: str = '/api/v1'

    @property
    def ADMIN_STR(self) -> str:
        return self.SECRET_KEY[-10:]

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    JWT_ALGORITHM: str = 'HS256'

    POSTGRES: Postgres = Postgres()

settings = Settings()
