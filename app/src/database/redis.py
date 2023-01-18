import redis.asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from src.config import config


class RedRedis:
    main_base = 0
    data_redis: ConnectionPool

    @classmethod
    async def connect_to_storage(cls):

        cls.data_redis = await aioredis.from_url(
            f"{config.RedisUrl}{cls.main_base}", decode_responses=True)


class DataRedis(RedRedis):

    @classmethod
    async def block_jwt(cls, key: str):
        return await cls.data_redis.set(key, "blocked", ex=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    @classmethod
    async def get_data(cls, key: str):
        return await cls.data_redis.get(key)
