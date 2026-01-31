import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from app.services.ScheduleService import get_schedule_by_master_id
from app.schemas.Schedule import ScheduleResponse


def _schedule_obj(sid=1, mid=1):
    attrs = {"id": sid, "master_id": mid}
    for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
        attrs[f"{day}_start"] = None
        attrs[f"{day}_end"] = None
    return type("Schedule", (), attrs)()


@pytest.mark.asyncio
class TestGetScheduleByMasterIdService:

    async def test_get_schedule_by_master_id_success(self):
        mock_session = AsyncMock()
        mock_schedule = _schedule_obj(1, 1)

        with patch("app.repositories.ScheduleRepository.read_schedule_by_master_id", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = mock_schedule

            result = await get_schedule_by_master_id(1, mock_session)
            mock_repo.assert_called_once_with(master_id=1, session=mock_session)
            assert isinstance(result, ScheduleResponse)
            assert result.id == 1
            assert result.master_id == 1

    async def test_get_schedule_by_master_id_not_found(self):
        mock_session = AsyncMock()
        with patch("app.repositories.ScheduleRepository.read_schedule_by_master_id", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = None

            with pytest.raises(HTTPException) as exc:
                await get_schedule_by_master_id(999, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Schedule not found"
