import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_async_engine(f"postgresql+asyncpg://webtron:webtron@db/webtron", echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_custom_sission():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
