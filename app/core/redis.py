# app/core/redis.py
from fastapi import Request
from redis import Redis
from settings import settings

redis_client: Redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


def get_redis_client() -> Redis:
    return redis_client


def get_redis(request: Request) -> Redis:
    """Зависимость FastAPI: возвращает Redis из app.state (в тестах можно подменить)."""
    return request.app.state.redis