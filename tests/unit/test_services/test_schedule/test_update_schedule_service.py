import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import time

from app.services.ScheduleService import update_schedule
from app.schemas.Schedule import ScheduleUpdate, ScheduleResponse


def _schedule_db_obj(sid=1, mid=1):
    attrs = {"id": sid, "master_id": mid, "monday_start": time(9, 0), "monday_end": time(18, 0)}
    for day in ("tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
        attrs[f"{day}_start"] = None
        attrs[f"{day}_end"] = None
    return type("Schedule", (), attrs)()


@pytest.mark.asyncio
class TestUpdateScheduleService:

    async def test_update_schedule_success(self):
        mock_session = AsyncMock()
        schedule_id = 1
        update_data = ScheduleUpdate(monday_start=time(9, 0), monday_end=time(18, 0))
        mock_schedule_db = _schedule_db_obj(schedule_id, 1)

        with patch("app.repositories.ScheduleRepository.read_schedule", new_callable=AsyncMock, return_value=mock_schedule_db) as mock_read, \
                patch("app.repositories.ScheduleRepository.update_schedule", new_callable=AsyncMock, return_value=mock_schedule_db) as mock_update:
            result = await update_schedule(schedule_id, update_data, mock_session)

            mock_read.assert_called_once_with(schedule_id=schedule_id, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, ScheduleResponse)

    async def test_update_schedule_not_found(self):
        mock_session = AsyncMock()
        with patch("app.repositories.ScheduleRepository.read_schedule", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await update_schedule(999, ScheduleUpdate(), mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Schedule not found"

    async def test_update_schedule_integrity_error(self):
        mock_session = AsyncMock()
        mock_schedule_db = _schedule_db_obj(1, 1)
        with patch("app.repositories.ScheduleRepository.read_schedule", new_callable=AsyncMock, return_value=mock_schedule_db), \
                patch("app.repositories.ScheduleRepository.update_schedule", new_callable=AsyncMock,
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_schedule(1, ScheduleUpdate(), mock_session)

            assert exc.value.status_code == 409
            assert "Schedule" in exc.value.detail
            mock_session.rollback.assert_called_once()
