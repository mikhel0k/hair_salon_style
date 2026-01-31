import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, time

from app.services.CellService import get_cells_by_date_and_master_id
from app.schemas.Cell import CellResponse, AllowedCellsStatuses


@pytest.mark.asyncio
class TestGetCellsByDateAndMasterIdService:

    async def test_get_cells_by_date_and_master_id_success(self):
        mock_session = AsyncMock()
        mock_cell = type("Cell", (), {"id": 1, "master_id": 1, "date": date(2025, 2, 1), "time": time(9, 0), "status": AllowedCellsStatuses.FREE})()

        with patch("app.repositories.CellRepository.read_cells_by_master_id_and_date", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = [mock_cell]

            result = await get_cells_by_date_and_master_id(
                master_id=1, search_date=date(2025, 2, 1), session=mock_session
            )
            mock_repo.assert_called_once_with(
                master_id=1, cell_date=date(2025, 2, 1), session=mock_session
            )
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], CellResponse)

    async def test_get_cells_by_date_and_master_id_empty(self):
        mock_session = AsyncMock()
        with patch("app.repositories.CellRepository.read_cells_by_master_id_and_date", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = []

            result = await get_cells_by_date_and_master_id(
                master_id=1, search_date=date(2025, 2, 1), session=mock_session
            )
            assert isinstance(result, list)
            assert len(result) == 0
