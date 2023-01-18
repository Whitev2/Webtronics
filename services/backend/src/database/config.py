from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import config
Base = declarative_base()


class Postgres:
    async_session: sessionmaker

    @classmethod
    async def connect_to_storage(cls):
        engine_pg = create_async_engine(config.PostgresUrl, echo=False)

        cls.async_session = sessionmaker(engine_pg, class_=AsyncSession, expire_on_commit=False)
