import redis.asyncio as aioredis
import time
from ..constants.redis_cache import REDIS_TIMEOUT, REDIS_RECONNECTION_ATEMPT_TIMEOUT


class AsyncRedis:
    __redis = None
    __last_connection_attempt = time.time()
    __connection_is_active = False

    @classmethod
    async def __try_reconnect(cls) -> None:
        cls.__connection_is_active = False

        if time.time() - cls.__last_connection_attempt > REDIS_RECONNECTION_ATEMPT_TIMEOUT:
            cls.__last_connection_attempt = time.time()

            try:
                cls.__redis = aioredis.Redis(host="redis", socket_connect_timeout=REDIS_TIMEOUT, socket_timeout=REDIS_TIMEOUT)

                await cls.__redis.ping()

                cls.__connection_is_active = True
            except Exception as e:
                print(f"Redis connection error: {e}")

    @classmethod
    async def safe_set(cls, key: str, value: str, ex: int) -> None:
        if cls.__connection_is_active:
            try:
                await cls.__redis.set(key, value, ex=ex)
            except Exception as e:
                print(f"Error setting key in Redis: {e}")

                await cls.__try_reconnect()
        else:
            await cls.__try_reconnect()

    @classmethod
    async def safe_get(cls, key: str) -> str | None:
        if cls.__connection_is_active:
            try:
                return await cls.__redis.get(key)
            except Exception as e:
                print(f"Error getting key from Redis: {e}")

                await cls.__try_reconnect()
        else:
            await cls.__try_reconnect()

    
        