import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.RecordService import new_record
from app.schemas.UserFlow import MakeRecord
from app.schemas.Record import RecordResponse, AllowedRecordStatuses


def _make_record_data():
    return MakeRecord(
        phone_number="+79009009090",
        master_id=1,
        service_id=1,
        cell_id=1,
        notes=None,
    )


@pytest.mark.asyncio
class TestNewRecordService:

    async def test_new_record_master_not_provides_service_409(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.checking_master_provides_service") as mock_check:
            mock_check.return_value = False

            with pytest.raises(HTTPException) as exc:
                await new_record(_make_record_data(), mock_session)

            mock_check.assert_called_once_with(
                master_id=1, session=mock_session, service_id=1
            )
            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail

    async def test_new_record_success_existing_user(self):
        mock_session = AsyncMock()
        data = _make_record_data()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_service = MagicMock()
        mock_service.duration_minutes = 30
        mock_cell = MagicMock()
        mock_cell.status = "FREE"
        mock_cell.master_id = 1
        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.master_id = 1
        mock_record.service_id = 1
        mock_record.user_id = 1
        mock_record.cell_id = 1
        mock_record.status = AllowedRecordStatuses.CREATED
        mock_record.notes = None

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock, return_value=mock_user), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]), \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock), \
                patch("app.repositories.RecordRepository.create_record", new_callable=AsyncMock, return_value=mock_record):
            result = await new_record(data, mock_session)

            mock_session.commit.assert_called_once()
            assert isinstance(result, RecordResponse)

    async def test_new_record_integrity_error_create_user_409(self):
        mock_session = AsyncMock()
        data = _make_record_data()
        mock_service = MagicMock()
        mock_service.duration_minutes = 30
        mock_cell = MagicMock()
        mock_cell.status = "FREE"
        mock_cell.master_id = 1

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock, return_value=None), \
                patch("app.repositories.UserRepository.create_user", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]):
            with pytest.raises(HTTPException) as exc:
                await new_record(data, mock_session)

            mock_session.rollback.assert_called_once()
            assert exc.value.status_code == 409
            assert "Record with this data already exists" in exc.value.detail

    async def test_new_record_integrity_error_create_record_500(self):
        mock_session = AsyncMock()
        data = _make_record_data()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_service = MagicMock()
        mock_service.duration_minutes = 30
        mock_cell = MagicMock()
        mock_cell.status = "FREE"
        mock_cell.master_id = 1

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock, return_value=mock_user), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]), \
                patch("app.repositories.CellRepository.update_cells", new_callable=AsyncMock), \
                patch("app.repositories.RecordRepository.create_record", new_callable=AsyncMock, side_effect=Exception("db error")):
            with pytest.raises(HTTPException) as exc:
                await new_record(data, mock_session)

            mock_session.rollback.assert_called_once()
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal server error"

    async def test_new_record_cell_occupied_409(self):
        mock_session = AsyncMock()
        data = _make_record_data()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_service = MagicMock()
        mock_service.duration_minutes = 30
        mock_cell = MagicMock()
        mock_cell.status = "OCCUPIED"
        mock_cell.master_id = 1

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock, return_value=mock_user), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]):
            with pytest.raises(HTTPException) as exc:
                await new_record(data, mock_session)

            assert exc.value.status_code == 409
            assert "Cell already occupied" in exc.value.detail

    async def test_new_record_cell_wrong_master_409(self):
        mock_session = AsyncMock()
        data = _make_record_data()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_service = MagicMock()
        mock_service.duration_minutes = 30
        mock_cell = MagicMock()
        mock_cell.status = "FREE"
        mock_cell.master_id = 999

        with patch("app.repositories.MasterRepository.checking_master_provides_service", new_callable=AsyncMock, return_value=True), \
                patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock, return_value=mock_user), \
                patch("app.repositories.ServiceRepository.read_service_by_id", new_callable=AsyncMock, return_value=mock_service), \
                patch("app.repositories.CellRepository.read_cells", new_callable=AsyncMock, return_value=[mock_cell]):
            with pytest.raises(HTTPException) as exc:
                await new_record(data, mock_session)

            assert exc.value.status_code == 409
            assert "Master not provides" in exc.value.detail
