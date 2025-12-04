from datetime import date, time

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from starlette import status

from app.models import User, Record
from app.services.RecordForUser import user_find_record
from app.schemas import UserFind, RecordResponse


class TestUserFindRecord:
    @pytest.mark.asyncio
    async def test_user_find_record_user_not_found(self):
        mock_session = AsyncMock()
        test_phone = "+79161234567"
        test_user_find = UserFind(phone_number=test_phone)

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository, \
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockUserRepository.read_user_by_phone = AsyncMock(return_value=None)

            with pytest.raises(HTTPException) as exc_info:
                await user_find_record(test_user_find, mock_session)

            exception = exc_info.value

            assert exception.status_code == status.HTTP_404_NOT_FOUND
            assert "User not found" in str(exception.detail)

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user=test_user_find,

            )
            MockRecordRepository.read_record_by_user_id.assert_not_called()


    @pytest.mark.asyncio
    async def test_user_find_record_user_found(self):
        mock_session = AsyncMock()
        test_phone = "+79161234567"
        user_id = 1
        test_user_find = UserFind(phone_number=test_phone)
        test_user = MagicMock()
        test_user.id = user_id
        test_user.phone_number = test_phone

        test_record = MagicMock()
        test_record.id = 1
        test_record.date = date.today()
        test_record.time = time(12, 0, 0)
        test_record.status = "created"
        test_record.price = 1.0
        test_record.notes = ""
        test_record.user_id = user_id

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository,\
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockUserRepository.read_user_by_phone = AsyncMock(return_value=test_user)
            MockRecordRepository.read_record_by_user_id = AsyncMock(return_value=[test_record,])

            result = await user_find_record(test_user_find, mock_session)

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], RecordResponse)

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user=test_user_find,
            )
            MockRecordRepository.read_record_by_user_id.assert_called_once_with(
                session=mock_session,
                user_id=user_id,
            )
