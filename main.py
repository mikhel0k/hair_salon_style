from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis import Redis

from app.core.logger import setup_logging
from settings import settings

setup_logging()

from app.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True,
    )
    app.state.redis = redis_client
    try:
        yield
    finally:
        redis_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
