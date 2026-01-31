import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.RecordService import update_status_to_cancelled
from app.schemas.Record import EditRecordStatus, RecordResponse, AllowedRecordStatuses


def _record_obj():
    r = SimpleNamespace(
        id=1, master_id=1, service_id=1, user_id=1, cell_id=1,
        status=AllowedRecordStatuses.CANCELLED, notes=None,
    )
    r.service = SimpleNamespace(duration_minutes=30)
    return r


@pytest.mark.asyncio
class TestUpdateStatusToCancelledService:

    async def test_update_status_to_cancelled_success(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CANCELLED)
        mock_record = _record_obj()
        mock_cell = type("Cell", (), {"master_id": 1, "status": "OCCUPIED"})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record) as mock_read, \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock) as mock_update, \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_record.service) as mock_svc, \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]) as mock_cells, \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock) as mock_update_cells:
            result = await update_status_to_cancelled(data, mock_session)

            mock_read.assert_called_once_with(record_id=1, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, RecordResponse)
            assert result.status == AllowedRecordStatuses.CANCELLED

    async def test_update_status_to_cancelled_not_found(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=999, status=AllowedRecordStatuses.CANCELLED)

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_cancelled(data, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Record not found"

    async def test_update_status_to_cancelled_wrong_status_403(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CONFIRMED)

        with pytest.raises(HTTPException) as exc:
            await update_status_to_cancelled(data, mock_session)

        assert exc.value.status_code == 403
        assert "Status not canceled" in exc.value.detail

    async def test_update_status_to_cancelled_integrity_error_update_record_409(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CANCELLED)
        mock_record = _record_obj()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_cancelled(data, mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()

    async def test_update_status_to_cancelled_integrity_error_update_cells_409(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CANCELLED)
        mock_record = _record_obj()
        mock_cell = type("Cell", (), {"master_id": 1, "status": "OCCUPIED"})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_record.service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]), \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_cancelled(data, mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()

    async def test_update_status_to_cancelled_cell_master_mismatch_409(self):
        mock_session = AsyncMock()
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CANCELLED)
        mock_record = _record_obj()
        mock_record.master_id = 1
        mock_cell = type("Cell", (), {"master_id": 999, "status": "OCCUPIED"})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_record.service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_cancelled(data, mock_session)

            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail
