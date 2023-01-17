from typing import Optional

from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    PostgresUrl: PostgresDsn = "postgresql+asyncpg://webtron:webtron@db:5432/webtron"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()