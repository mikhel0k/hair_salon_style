import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, time
from fastapi import HTTPException

from app.services.CellService import get_ids_with_empty_cells_by_service_id_master_id_in_date
from app.schemas.Cell import CellResponse, AllowedCellsStatuses


@pytest.mark.asyncio
class TestGetIdsWithEmptyCellsByServiceIdMasterIdInDateService:

    async def test_get_slots_master_not_provides_service_409(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock) as mock_check:
            mock_check.return_value = False

            with pytest.raises(HTTPException) as exc:
                await get_ids_with_empty_cells_by_service_id_master_id_in_date(
                    record_date=date(2025, 2, 1),
                    service_id=1,
                    master_id=1,
                    session=mock_session,
                )

            mock_check.assert_called_once_with(
                master_id=1, session=mock_session, service_id=1
            )
            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail

    async def test_get_slots_service_not_found_404(self):
        mock_session = AsyncMock()
        mock_cell = type("Cell", (), {"id": 1, "master_id": 1, "date": date(2025, 2, 1), "time": time(9, 0), "status": AllowedCellsStatuses.FREE})()
        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.CellRepository.read_cells_by_master_id_and_date", new_callable=AsyncMock, return_value=[mock_cell]), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await get_ids_with_empty_cells_by_service_id_master_id_in_date(
                    record_date=date(2025, 2, 1),
                    service_id=999,
                    master_id=1,
                    session=mock_session,
                )

            assert exc.value.status_code == 404
            assert exc.value.detail == "Service not found"

    async def test_get_slots_no_cells_returns_message(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.CellRepository.read_cells_by_master_id_and_date", new_callable=AsyncMock, return_value=[]):
            result = await get_ids_with_empty_cells_by_service_id_master_id_in_date(
                record_date=date(2025, 2, 1),
                service_id=1,
                master_id=1,
                session=mock_session,
            )
            assert result == {"message": "No free cells found"}

    async def test_get_slots_success_returns_list(self):
        mock_session = AsyncMock()
        mock_cell = type("Cell", (), {"id": 1, "master_id": 1, "date": date(2025, 2, 1), "time": time(9, 0), "status": AllowedCellsStatuses.FREE})()
        mock_service = type("Service", (), {"duration_minutes": 30})()

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.CellRepository.read_cells_by_master_id_and_date",
                      new_callable=AsyncMock, return_value=[mock_cell, mock_cell]), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service):
            result = await get_ids_with_empty_cells_by_service_id_master_id_in_date(
                record_date=date(2025, 2, 1),
                service_id=1,
                master_id=1,
                session=mock_session,
            )
            assert isinstance(result, list)
            assert len(result) >= 0
            if result:
                assert isinstance(result[0], CellResponse)
