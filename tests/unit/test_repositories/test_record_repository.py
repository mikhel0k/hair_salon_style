import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date

from app.repositories.RecordRepository import (
    create_record,
    read_record_by_id,
    read_records_by_master_id,
    read_records_by_master_id_and_time_interval,
    read_records_by_servise_id,
    read_records_by_user_id,
    read_record_by_cell_id,
    update_record,
)
from app.models.Record import Record, AllowedRecordStatuses


def _mock_record():
    r = MagicMock(spec=Record)
    r.id = 1
    r.master_id = 1
    r.service_id = 1
    r.user_id = 1
    r.cell_id = 1
    r.status = AllowedRecordStatuses.CREATED
    r.notes = None
    return r


@pytest.mark.asyncio
class TestRecordRepository:

    async def test_create_record(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        record = _mock_record()

        result = await create_record(record, session)

        session.add.assert_called_once_with(record)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(record)
        assert result is record

    async def test_read_record_by_id(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=_mock_record())

        result = await read_record_by_id(1, session)

        session.get.assert_called_once()
        assert result is not None
        assert result.id == 1

    async def test_read_record_by_id_not_found(self):
        session = AsyncMock()
        session.get = AsyncMock(return_value=None)

        result = await read_record_by_id(999, session)

        assert result is None

    async def test_read_records_by_master_id(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_record()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_records_by_master_id(1, session)

        session.execute.assert_called_once()
        assert len(result) == 1
        assert result[0].id == 1

    async def test_read_records_by_master_id_and_time_interval(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_record()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_records_by_master_id_and_time_interval(
            master_id=1,
            date_start=date(2025, 1, 1),
            date_end=date(2025, 1, 31),
            session=session,
        )

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_records_by_servise_id(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_record()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_records_by_servise_id(1, session)

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_records_by_user_id(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_record()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_records_by_user_id(1, session)

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_read_record_by_cell_id(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [_mock_record()]
        session.execute = AsyncMock(return_value=mock_result)

        result = await read_record_by_cell_id(1, session)

        session.execute.assert_called_once()
        assert len(result) == 1

    async def test_update_record(self):
        session = MagicMock()
        session.add = MagicMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        record = _mock_record()

        result = await update_record(record, session)

        session.add.assert_called_once_with(record)
        session.flush.assert_called_once()
        session.refresh.assert_called_once_with(record)
        assert result is record
