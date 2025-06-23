import redis.asyncio as aioredis
import time
from ..constants.redis_cache import REDIS_TIMEOUT, REDIS_RECONNECTION_ATEMPT_TIMEOUT


class AsyncRedis:
    redis = None
    last_connection_attempt = time.time()
    connection_is_active = False

    @classmethod
    async def __try_reconnect(cls) -> None:
        cls.connection_is_active = False

        if time.time() - cls.last_connection_attempt > REDIS_RECONNECTION_ATEMPT_TIMEOUT:
            cls.last_connection_attempt = time.time()

            try:
                cls.redis = aioredis.Redis(host="redis", socket_connect_timeout=REDIS_TIMEOUT, socket_timeout=REDIS_TIMEOUT)

                await cls.redis.ping()

                cls.connection_is_active = True
            except:
                ...

    @classmethod
    async def safe_set(cls, key: str, value: str, ex: int) -> None:
        if cls.connection_is_active:
            try:
                await cls.redis.set(key, value, ex=ex)
            except:
                await cls.__try_reconnect()
        else:
            await cls.__try_reconnect()

    @classmethod
    async def safe_get(cls, key: str) -> str | None:
        if cls.connection_is_active:
            try:
                return await cls.redis.get(key)
            except:
                await cls.__try_reconnect()
        else:
            await cls.__try_reconnect()

    
        