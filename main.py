from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import setup_logging

setup_logging()

from app.api import router


@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
