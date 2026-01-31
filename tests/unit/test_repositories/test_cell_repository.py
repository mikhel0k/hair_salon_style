import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date, time

from app.repositories.CellRepository import (
    create_cell,
    create_cells,
    read_cell,
    read_cells,
    read_free_cells_by_master_id_and_date,
    read_cells_by_master_id_and_date,
    read_cells_by_master_id,
    update_cell,
    update_cells,
)
from app.models.Cell import Cell


def _mock_cell():
    c = MagicMock(spec=Cell)
    c.id = 1
    c.master_id = 1
    c.date = date(2025, 1, 1)
    c.time = time(9, 0)
    c.status = "FREE"
    return c


@pytest.mark.asyncio
class TestCellRepository:

    async def test_create_cell(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        cell = _mock_cell()

        result = await create_cell(cell, session)

        session.add.assert_called_once_with(cell)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(cell)
        assert result is cell

    async def test_create_cells(self):
        session = MagicMock()
        session.add_all = MagicMock()
        session.flush = AsyncMock()
        cells = [_mock_cell(), _mock_cell()]

        await create_cells(cells, session)

        session.add_all.assert_called_once_with(cells)
        session.flush.assert_called_once()

    async def test_read_cell(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=_mock_cell())

        result = await read_cell(1, session)

        session.get.assert_called_once()
        assert result is not None
        assert result.id == 1

    async def test_read_cell_not_found(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=None)

        result = await read_cell(999, session)

        assert result is None

    async def test_read_cells(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_cell()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_cells([1, 2], session)

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_free_cells_by_master_id_and_date(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_cell()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_free_cells_by_master_id_and_date(
            master_id=1,
            cell_date=date(2025, 1, 1),
            session=session,
        )

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_cells_by_master_id_and_date(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_cell()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_cells_by_master_id_and_date(
            master_id=1,
            cell_date=date(2025, 1, 1),
            session=session,
        )

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_cells_by_master_id(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_cell()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_cells_by_master_id(master_id=1, session=session)

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_update_cell(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        cell = _mock_cell()

        result = await update_cell(cell, session)

        session.add.assert_called_once_with(cell)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(cell)
        assert result is cell

    async def test_update_cells(self):
        session = MagicMock()
        session.add_all = MagicMock()
        session.flush = AsyncMock()
        cells = [_mock_cell(), _mock_cell()]

        await update_cells(cells, session)

        session.add_all.assert_called_once_with(cells)
        session.flush.assert_called_once()
