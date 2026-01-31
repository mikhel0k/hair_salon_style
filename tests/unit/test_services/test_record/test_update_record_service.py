import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.RecordService import update_record
from app.schemas.Record import RecordUpdate, RecordResponse, AllowedRecordStatuses


@pytest.mark.asyncio
class TestUpdateRecordService:

    async def test_update_record_not_found_404(self):
        mock_session = AsyncMock()
        update_data = RecordUpdate(notes="New note")

        with patch("app.services.RecordService.RecordRepository.read_record_by_id", new_callable=AsyncMock) as mock_read:
            mock_read.return_value = None

            with pytest.raises(HTTPException) as exc:
                await update_record(999, update_data, mock_session)

            mock_read.assert_called_once_with(999, mock_session)
            assert exc.value.status_code == 404
            assert "Record not found" in str(exc.value.detail)

    async def test_update_record_success_notes_only(self):
        mock_session = AsyncMock()
        record_id = 1
        update_data = RecordUpdate(notes="New note")
        mock_record = type("Record", (), {
            "id": record_id, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1,
            "status": AllowedRecordStatuses.CREATED, "notes": "New note",
            "service": type("S", (), {"duration_minutes": 30})(),
        })()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock) as mock_update:
            result = await update_record(record_id, update_data, mock_session)

            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, RecordResponse)
            assert result.notes == "New note"

    async def test_update_record_integrity_error_409(self):
        mock_session = AsyncMock()
        mock_record = type("Record", (), {"id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1, "status": AllowedRecordStatuses.CREATED, "notes": None, "service": type("S", (), {"duration_minutes": 30})()})()
        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_record(1, RecordUpdate(notes="X"), mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()

    async def test_update_record_master_id_without_cell_id_409(self):
        mock_session = AsyncMock()
        mock_record = type("Record", (), {"id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1, "status": AllowedRecordStatuses.CREATED, "notes": None, "service": type("S", (), {"duration_minutes": 30})()})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True):
            with pytest.raises(HTTPException) as exc:
                await update_record(1, RecordUpdate(master_id=2), mock_session)

            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail

    async def test_update_record_cell_change_integrity_error_409(self):
        mock_session = AsyncMock()
        mock_record = type("Record", (), {"id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1, "status": AllowedRecordStatuses.CREATED, "notes": None, "service": type("S", (), {"duration_minutes": 30})()})()
        mock_old_cell = type("Cell", (), {"master_id": 1, "status": "OCCUPIED"})()
        mock_new_cell = type("Cell", (), {"master_id": 1, "status": "FREE"})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_record.service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, side_effect=[[mock_old_cell], [mock_new_cell]]), \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_record(1, RecordUpdate(cell_id=2), mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()

    async def test_update_record_new_cell_already_occupied_409(self):
        mock_session = AsyncMock()
        mock_record = type("Record", (), {"id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1, "status": AllowedRecordStatuses.CREATED, "notes": None, "service": type("S", (), {"duration_minutes": 30})()})()
        mock_old_cell = type("Cell", (), {"master_id": 1, "status": "OCCUPIED"})()
        mock_new_cell = type("Cell", (), {"master_id": 1, "status": "OCCUPIED"})()

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_record.service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, side_effect=[[mock_old_cell], [mock_new_cell]]), \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock):
            with pytest.raises(HTTPException) as exc:
                await update_record(1, RecordUpdate(cell_id=2), mock_session)

            assert exc.value.status_code == 409
            assert "Cell already occupied" in exc.value.detail
