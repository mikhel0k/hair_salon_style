from dataclasses import dataclass

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from alembic.config import Config
from alembic import command

from main import app
from app.core import get_session
from settings import settings

@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        future=True
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def setup_db(test_engine):
    alembic_cfg = Config("alembic.ini")

    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.TEST_DATABASE_URL
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: _run_upgrade(alembic_cfg, sync_conn))

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: _run_downgrade(alembic_cfg, sync_conn))


def _run_upgrade(config, connection):
    config.attributes["connection"] = connection
    command.upgrade(config, "head")


def _run_downgrade(config, connection):
    config.attributes["connection"] = connection
    command.downgrade(config, "base")


@pytest.fixture(scope="function")
async def ac(test_engine) -> AsyncGenerator[AsyncClient, None]:
    session_factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False
    )
    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()


RIGHT_LOGIN = "I_am_admin"
RIGHT_PASSWORD = "Zxc-q123"
