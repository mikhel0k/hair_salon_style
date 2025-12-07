from datetime import date, time
from unittest.mock import MagicMock, AsyncMock, patch

import pytest
from fastapi import HTTPException, status

from app.schemas import EditRecordStatus, RecordResponse
from app.services import switch_status_of_record


class TestSwitchStatusOfRecord:
    @pytest.mark.asyncio
    async def test_switch_status(self):
        mock_session = MagicMock()

        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock()
        mock_context.__aexit__ = AsyncMock()

        mock_session.begin.return_value = mock_context

        date_record = date.today()
        time_record = time(hour=23, minute=59, second=59)
        notes = "I want to drink beer while getting a haircut"
        user_id = 1

        test_record = MagicMock()
        test_record.id = 1
        test_record.date = date_record
        test_record.time = time_record
        test_record.status = "created"
        test_record.price = 0
        test_record.notes = notes
        test_record.user_id = user_id

        test_record_rejected = MagicMock()
        test_record_rejected.id = 1
        test_record_rejected.date = date_record
        test_record_rejected.time = time_record
        test_record_rejected.status = "rejected"
        test_record_rejected.price = 0
        test_record_rejected.notes = notes
        test_record_rejected.user_id = user_id

        info_record = EditRecordStatus(
            id=1,
            status="rejected",
        )

        with patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockRecordRepository.read_record_by_id = AsyncMock(return_value=test_record)
            MockRecordRepository.update_record_status = AsyncMock(return_value=test_record_rejected)

            result = await switch_status_of_record(info_record=info_record, session=mock_session)

            assert isinstance(result, RecordResponse)

            MockRecordRepository.read_record_by_id.assert_called_once_with(
                session=mock_session,
                record_id=info_record.id,
            )
            MockRecordRepository.update_record_status.assert_called_once_with(
                session=mock_session,
                record=test_record,
                new_status="rejected",
            )

            assert result.id == test_record_rejected.id
            assert result.date == test_record_rejected.date
            assert result.time == test_record_rejected.time
            assert result.status == test_record_rejected.status
            assert result.price == test_record_rejected.price
            assert result.notes == test_record_rejected.notes
            assert result.user_id == test_record_rejected.user_id

    @pytest.mark.asyncio
    async def test_switch_status_wrong_id(self):
        mock_session = MagicMock()

        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock()
        mock_context.__aexit__ = AsyncMock(return_value=False)

        mock_session.begin.return_value = mock_context


        info_record = EditRecordStatus(
            id=3,
            status="rejected",
        )

        with patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockRecordRepository.read_record_by_id = AsyncMock(return_value=None)
            MockRecordRepository.update_record_status = AsyncMock(return_value=None)

            with pytest.raises(HTTPException) as exc_info:
                await switch_status_of_record(info_record, mock_session)

            exception = exc_info.value

            assert exception.status_code == status.HTTP_404_NOT_FOUND
            assert "Record not found" in str(exception.detail)

            MockRecordRepository.read_record_by_id.assert_called_once_with(
                session=mock_session,
                record_id=info_record.id,
            )

            MockRecordRepository.update_record_status.assert_not_called()
