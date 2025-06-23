import redis.asyncio as aioredis


async_redis = aioredis.Redis(host="redis")
