import pytest
from unittest.mock import AsyncMock, patch
from datetime import date

from app.services.RecordService import read_records_by_master_id_and_time_interval
from app.schemas.Record import RecordResponse


@pytest.mark.asyncio
class TestReadRecordsByMasterIdAndTimeIntervalService:

    async def test_read_records_by_master_id_and_time_interval_success(self):
        mock_session = AsyncMock()
        master_id = 1
        start_time = date(2025, 2, 1)
        mock_record = AsyncMock()
        mock_record.id = 1
        mock_record.master_id = master_id
        mock_record.service_id = 1
        mock_record.user_id = 1
        mock_record.cell_id = 1
        mock_record.status = "CREATED"
        mock_record.notes = None

        with patch("app.repositories.RecordRepository.read_records_by_master_id_and_time_interval") as mock_repo:
            mock_repo.return_value = [mock_record]

            result = await read_records_by_master_id_and_time_interval(
                master_id=master_id,
                start_time=start_time,
                session=mock_session,
            )
            mock_repo.assert_called_once()
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], RecordResponse)

    async def test_read_records_by_master_id_and_time_interval_empty(self):
        mock_session = AsyncMock()
        with patch("app.repositories.RecordRepository.read_records_by_master_id_and_time_interval") as mock_repo:
            mock_repo.return_value = []

            result = await read_records_by_master_id_and_time_interval(
                master_id=1,
                start_time=date(2025, 2, 1),
                session=mock_session,
            )
            assert isinstance(result, list)
            assert len(result) == 0
