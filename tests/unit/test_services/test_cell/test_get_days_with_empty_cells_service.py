import pytest
from unittest.mock import AsyncMock, patch
from datetime import date
from fastapi import HTTPException

from app.services.CellService import get_days_with_empty_cells_by_service_id_and_master_id


@pytest.mark.asyncio
class TestGetDaysWithEmptyCellsByServiceIdAndMasterIdService:

    async def test_get_days_master_not_provides_service_409(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.checking_master_provides_service") as mock_check:
            mock_check.return_value = False

            with pytest.raises(HTTPException) as exc:
                await get_days_with_empty_cells_by_service_id_and_master_id(
                    service_id=1, master_id=1, session=mock_session
                )

            mock_check.assert_called_once_with(
                master_id=1, session=mock_session, service_id=1
            )
            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail

    async def test_get_days_service_not_found_404(self):
        mock_session = AsyncMock()
        mock_cell = AsyncMock()
        mock_cell.date = date(2025, 2, 1)
        mock_cell.status = "FREE"

        with patch("app.repositories.MasterRepository.checking_master_provides_service", return_value=True), \
                patch("app.repositories.CellRepository.read_cells_by_master_id", return_value=[mock_cell]), \
                patch("app.repositories.ServiceRepository.read_service_by_id", return_value=None):
            with pytest.raises(HTTPException) as exc:
                await get_days_with_empty_cells_by_service_id_and_master_id(
                    service_id=999, master_id=1, session=mock_session
                )

            assert exc.value.status_code == 404
            assert exc.value.detail == "Service not found"

    async def test_get_days_no_cells_returns_message(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.checking_master_provides_service", return_value=True), \
                patch("app.repositories.CellRepository.read_cells_by_master_id", return_value=[]):
            result = await get_days_with_empty_cells_by_service_id_and_master_id(
                service_id=1, master_id=1, session=mock_session
            )
            assert result == {"message": "No free cells found"}
