import redis.asyncio as aioredis
import time
import logging
from ..constants.redis_cache import REDIS_TIMEOUT, REDIS_RECONNECTION_ATEMPT_TIMEOUT


logger = logging.getLogger(__name__)


class AsyncRedis:
    _redis = None
    _last_connection_attempt = time.time()
    _connection_is_active = False

    @classmethod
    async def _try_reconnect(cls) -> None:
        cls._connection_is_active = False

        if (
            time.time() - cls._last_connection_attempt
            > REDIS_RECONNECTION_ATEMPT_TIMEOUT
        ):
            cls._last_connection_attempt = time.time()

            try:
                cls._redis = aioredis.Redis(
                    host="redis",
                    socket_connect_timeout=REDIS_TIMEOUT,
                    socket_timeout=REDIS_TIMEOUT,
                )

                await cls._redis.ping()

                cls._connection_is_active = True
            except aioredis.ConnectionError as e:
                logger.error(f"Connection error: {e}")

    @classmethod
    async def safe_set(cls, key: str, value: str, ex: int) -> None:
        if cls._connection_is_active:
            try:
                await cls._redis.set(key, value, ex=ex)
            except aioredis.ConnectionError as e:
                logger.error(f"Failed to set: {e}")

                await cls._try_reconnect()
        else:
            await cls._try_reconnect()

    @classmethod
    async def safe_get(cls, key: str) -> str | None:
        if cls._connection_is_active:
            try:
                return await cls._redis.get(key)
            except aioredis.ConnectionError as e:
                logger.error(f"Failed to get: {e}")

                await cls._try_reconnect()
        else:
            await cls._try_reconnect()
