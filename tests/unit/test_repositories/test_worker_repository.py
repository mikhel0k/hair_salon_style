import pytest
from unittest.mock import AsyncMock, MagicMock

from app.repositories.WorkerRepository import (
    create_worker,
    get_worker,
    get_worker_by_username,
    update_worker,
    get_worker_full,
)
from app.models.Worker import Worker


def _mock_worker():
    w = MagicMock(spec=Worker)
    w.id = 1
    w.username = "admin"
    w.master_id = None
    w.is_master = False
    w.is_admin = True
    w.is_active = True
    return w


@pytest.mark.asyncio
class TestWorkerRepository:

    async def test_create_worker(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        worker = _mock_worker()

        result = await create_worker(worker, session)

        session.add.assert_called_once_with(worker)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(worker)
        assert result is worker

    async def test_get_worker(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=_mock_worker())

        result = await get_worker(1, session)

        session.get.assert_called_once()
        assert result is not None
        assert result.id == 1

    async def test_get_worker_not_found(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=None)

        result = await get_worker(999, session)

        assert result is None

    async def test_get_worker_by_username(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = _mock_worker()
        session.execute = AsyncMock(return_value=mock_result)

        result = await get_worker_by_username("admin", session)

        session.execute.assert_called_once()
        assert result is not None
        assert result.username == "admin"

    async def test_get_worker_by_username_not_found(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await get_worker_by_username("unknown", session)

        assert result is None

    async def test_update_worker(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        worker = _mock_worker()

        result = await update_worker(worker, session)

        session.add.assert_called_once_with(worker)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(worker)
        assert result is worker

    async def test_get_worker_full(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = _mock_worker()
        session.execute = AsyncMock(return_value=mock_result)

        result = await get_worker_full(1, session)

        session.execute.assert_called_once()
        assert result is not None
        assert result.id == 1
