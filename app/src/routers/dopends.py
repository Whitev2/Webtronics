from src.crud.post_crud import PostCrud
from src.crud.user_crud import UserCrud
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import Postgres


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with Postgres().async_session() as session:
        yield session
        await session.commit()
