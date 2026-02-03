import os

os.environ.setdefault("SEND_LOGIN_CODE_EMAIL", "false")

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from redis import Redis
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

    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True,
    )
    app.state.redis = redis_client

    app.dependency_overrides[get_session] = override_get_session
    try:
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as client:
            yield client
    finally:
        redis_client.close()
        app.dependency_overrides.clear()

CORRECT_LOGIN = "I_am_admin"
CORRECT_PASSWORD = "Zxc-q123"


@pytest.fixture
def redis_client(ac: AsyncClient):
    """Redis из app.state. Получить код по jti после try_login: redis_client.get(f'login_confirm_jti:{jti}')."""
    return app.state.redis


@pytest.fixture
async def token(ac: AsyncClient, redis_client):
    """Логин по паролю -> код из Redis -> login_confirm -> access_token в cookie."""
    login_payload = {"username": CORRECT_LOGIN, "password": CORRECT_PASSWORD}
    resp_login = await ac.post("/v1/auth/login/", json=login_payload)
    assert resp_login.status_code == 200, resp_login.text
    jti = resp_login.json()
    code = redis_client.get(f"login_confirm_jti:{jti}")
    assert code, "Код не найден в Redis (login_confirm_jti)"
    resp_confirm = await ac.post("/v1/auth/login/confirm/", json={"code": code, "jti": jti})
    assert resp_confirm.status_code == 200, resp_confirm.text
    access_token = resp_confirm.cookies.get("access_token")
    assert access_token
    return {"Cookie": f"access_token={access_token}"}
