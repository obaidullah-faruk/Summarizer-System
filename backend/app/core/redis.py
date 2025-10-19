from redis.asyncio import Redis, ConnectionPool
from app.core.logging import logger
from app.core.config import get_settings

settings = get_settings()
pool: ConnectionPool | None = None
redis_client: Redis | None = None

def get_redis_client() -> Redis:
    return redis_client

async def initialize_redis():
    global redis_client
    redis_url = f"redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}"
    redis_client = Redis.from_url(redis_url, decode_responses=True)
    await redis_client.ping()
    logger.info("Redis client initialized successfully.")

async def close_redis():
    if redis_client:
        await redis_client.close()
        logger.info("Redis client closed successfully.")