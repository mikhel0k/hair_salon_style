import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.RecordService import update_status_to_completed_or_confirmed
from app.schemas.Record import EditRecordStatus, RecordResponse, AllowedRecordStatuses


def _record_obj(master_id=1, status=AllowedRecordStatuses.CONFIRMED):
    return type("Record", (), {
        "id": 1, "master_id": master_id, "service_id": 1, "user_id": 1, "cell_id": 1,
        "status": status, "notes": None,
    })()


@pytest.mark.asyncio
class TestUpdateStatusToCompletedOrConfirmedService:

    async def test_update_status_to_completed_or_confirmed_success(self):
        mock_session = AsyncMock()
        master_id = 1
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CONFIRMED)
        mock_record = _record_obj(master_id, AllowedRecordStatuses.CONFIRMED)

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record) as mock_read, \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock) as mock_update:
            result = await update_status_to_completed_or_confirmed(master_id, data, mock_session)

            mock_read.assert_called_once_with(record_id=1, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, RecordResponse)
            assert result.status.value == "CONFIRMED"

    async def test_update_status_to_completed_or_confirmed_wrong_master_403(self):
        mock_session = AsyncMock()
        master_id = 1
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CONFIRMED)
        mock_record = _record_obj(master_id=999)

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_completed_or_confirmed(master_id, data, mock_session)

            assert exc.value.status_code == 403
            assert "Record is not this master" in exc.value.detail

    async def test_update_status_to_completed_or_confirmed_integrity_error_409(self):
        mock_session = AsyncMock()
        master_id = 1
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.COMPLETED)
        mock_record = _record_obj(master_id, AllowedRecordStatuses.COMPLETED)

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock,
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_completed_or_confirmed(master_id, data, mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()

    async def test_update_status_to_completed_or_confirmed_wrong_status_403(self):
        mock_session = AsyncMock()
        master_id = 1
        data = EditRecordStatus(id=1, status=AllowedRecordStatuses.CANCELLED)

        with pytest.raises(HTTPException) as exc:
            await update_status_to_completed_or_confirmed(master_id, data, mock_session)

        assert exc.value.status_code == 403
        assert "Status not canceled" in exc.value.detail

    async def test_update_status_to_completed_or_confirmed_not_found_404(self):
        mock_session = AsyncMock()
        master_id = 1
        data = EditRecordStatus(id=999, status=AllowedRecordStatuses.CONFIRMED)

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await update_status_to_completed_or_confirmed(master_id, data, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Record not found"
