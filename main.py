from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import setup_logging
from app.core.redis import get_redis_client
from app.api import router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = get_redis_client()
    try:
        yield
    finally:
        get_redis_client().close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
