from typing import Optional

from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Config(BaseSettings):
    PostgresUrl: PostgresDsn
    RedisUrl: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str
    ALGORITHM: str
    HAND_EMAIL_API: str


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
