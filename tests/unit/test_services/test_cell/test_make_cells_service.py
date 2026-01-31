import pytest
from unittest.mock import AsyncMock, patch
from datetime import time
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.CellService import make_cells
from app.schemas.Schedule import ScheduleResponse


@pytest.mark.asyncio
class TestMakeCellsService:

    async def test_make_cells_not_found(self):
        mock_session = AsyncMock()
        with patch("app.repositories.ScheduleRepository.read_schedule_by_master_id", new_callable=AsyncMock) as mock_read:
            mock_read.return_value = None

            with pytest.raises(HTTPException) as exc:
                await make_cells(999, mock_session)

            mock_read.assert_called_once_with(master_id=999, session=mock_session)
            assert exc.value.status_code == 404

    async def test_make_cells_integrity_error(self):
        mock_session = AsyncMock()
        schedule_obj = ScheduleResponse(
            id=1, master_id=1,
            monday_start=time(9, 0), monday_end=time(12, 0),
            tuesday_start=None, tuesday_end=None,
            wednesday_start=None, wednesday_end=None,
            thursday_start=None, thursday_end=None,
            friday_start=None, friday_end=None,
            saturday_start=None, saturday_end=None,
            sunday_start=None, sunday_end=None,
        )

        with patch("app.repositories.ScheduleRepository.read_schedule_by_master_id", new_callable=AsyncMock, return_value=schedule_obj), \
                patch("app.repositories.CellRepository.create_cells", new_callable=AsyncMock) as mock_create:
            mock_create.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                await make_cells(1, mock_session)

            assert exc.value.status_code == 409
            assert "Cell" in exc.value.detail
            mock_session.rollback.assert_called_once()
