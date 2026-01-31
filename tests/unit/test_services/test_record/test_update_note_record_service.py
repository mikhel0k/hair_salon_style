import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.RecordService import update_note_record
from app.schemas.Record import EditRecordNote, RecordResponse, AllowedRecordStatuses


def _record_obj(notes="New note"):
    return type("Record", (), {
        "id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1,
        "status": AllowedRecordStatuses.CREATED, "notes": notes,
    })()


@pytest.mark.asyncio
class TestUpdateNoteRecordService:

    async def test_update_note_record_success(self):
        mock_session = AsyncMock()
        data = EditRecordNote(id=1, notes="New note")
        mock_record = _record_obj("New note")

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record) as mock_read, \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock) as mock_update:
            result = await update_note_record(data, mock_session)

            mock_read.assert_called_once_with(record_id=1, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, RecordResponse)
            assert result.notes == "New note"

    async def test_update_note_record_not_found(self):
        mock_session = AsyncMock()
        data = EditRecordNote(id=999, notes="Note")

        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await update_note_record(data, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Record not found"

    async def test_update_note_record_integrity_error(self):
        mock_session = AsyncMock()
        data = EditRecordNote(id=1, notes="Note")
        mock_record = _record_obj("Note")
        with patch("app.repositories.RecordRepository.read_record_by_id", new_callable=AsyncMock, return_value=mock_record), \
                patch("app.repositories.RecordRepository.update_record", new_callable=AsyncMock,
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_note_record(data, mock_session)

            assert exc.value.status_code == 409
            mock_session.rollback.assert_called_once()
