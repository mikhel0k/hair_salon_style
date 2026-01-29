import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from main import app
from app.core import get_session
from settings import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine(event_loop):
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def setup_db(engine):
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: command.upgrade(alembic_cfg, "head"))
    yield

@pytest.fixture(scope="function")
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    async with engine.connect() as connection:
        trans = await connection.begin()
        session = AsyncSession(bind=connection, expire_on_commit=False)

        yield session

        if trans.is_active:
            await trans.rollback()
        await session.close()


@pytest.fixture(scope="function")
async def ac(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()

CORRECT_LOGIN = "I_am_admin"
CORRECT_PASSWORD = "Zxc-q123"


@pytest.fixture
async def token(ac: AsyncClient):
    login_payload = {"username": CORRECT_LOGIN, "password": CORRECT_PASSWORD}
    response = await ac.post("/v1/auth/login/", json=login_payload)
    token = response.cookies.get("access_token")
    return {"Cookie": f"access_token={token}"}
