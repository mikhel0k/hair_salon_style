import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, time
from decimal import Decimal
from fastapi import HTTPException

from app.services.RecordService import get_records_by_phone
from app.schemas.User import UserFind
from app.schemas.Record import FullRecordResponse, AllowedRecordStatuses
from app.schemas.Master import AllowedMasterStatuses


def _full_record_obj():
    master = type("M", (), {"id": 1, "name": "Petr", "specialization_id": 1, "phone": "+79009009090", "email": "petr@mail.ru", "status": AllowedMasterStatuses.ACTIVE})()
    service = type("S", (), {"id": 1, "name": "Haircut", "price": Decimal("500"), "description": "Cut"})()

    class CellObj:
        id = 1
        master_id = 1
        date = date(2025, 2, 1)
        time = time(9, 0)
        status = "FREE"

    return type("Record", (), {
        "id": 1, "master_id": 1, "service_id": 1, "user_id": 1, "cell_id": 1,
        "status": AllowedRecordStatuses.CREATED, "notes": None,
        "master": master, "service": service, "cell": CellObj(),
    })()


@pytest.mark.asyncio
class TestGetRecordsByPhoneService:

    async def test_get_records_by_phone_success(self):
        mock_session = AsyncMock()
        user_find = UserFind(phone_number="+79009009090")
        mock_user = type("User", (), {"id": 1})()
        mock_record = _full_record_obj()

        with patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock) as mock_user_repo, \
                patch("app.repositories.RecordRepository.read_records_by_user_id", new_callable=AsyncMock) as mock_record_repo:
            mock_user_repo.return_value = mock_user
            mock_record_repo.return_value = [mock_record]

            result = await get_records_by_phone(user_find, mock_session)

            mock_user_repo.assert_called_once_with(user=user_find, session=mock_session)
            mock_record_repo.assert_called_once_with(user_id=1, session=mock_session)
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], FullRecordResponse)

    async def test_get_records_by_phone_user_not_found(self):
        mock_session = AsyncMock()
        user_find = UserFind(phone_number="+79009009090")

        with patch("app.repositories.UserRepository.read_user_by_phone", new_callable=AsyncMock) as mock_user_repo:
            mock_user_repo.return_value = None

            with pytest.raises(HTTPException) as exc:
                await get_records_by_phone(user_find, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "User not found"
