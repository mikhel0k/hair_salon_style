from datetime import date, time

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from starlette import status

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
        test_record.price = 400.50
        test_record.notes = "I want to drink beer while getting a haircut"
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

            assert result[0].id == test_record.id
            assert result[0].date == test_record.date
            assert result[0].time == test_record.time
            assert result[0].status == test_record.status
            assert result[0].notes == test_record.notes
            assert result[0].user_id == test_record.user_id


    @pytest.mark.asyncio
    async def test_user_find_some_record(self):
        mock_session = AsyncMock()
        test_phone = "+79161234567"
        user_id = 1
        test_user_find = UserFind(phone_number=test_phone)
        test_user = MagicMock()
        test_user.id = user_id
        test_user.phone_number = test_phone

        test_record_1 = MagicMock()
        test_record_1.id = 1
        test_record_1.date = date.today()
        test_record_1.time = time(12, 0, 0)
        test_record_1.status = "created"
        test_record_1.price = 1.0
        test_record_1.notes = ""
        test_record_1.user_id = user_id

        test_record_2 = MagicMock()
        test_record_2.id = 2
        test_record_2.date = date.today()
        test_record_2.time = time(12, 0, 0)
        test_record_2.status = "created"
        test_record_2.price = 1.0
        test_record_2.notes = ""
        test_record_2.user_id = user_id

        test_record_3 = MagicMock()
        test_record_3.id = 3
        test_record_3.date = date.today()
        test_record_3.time = time(12, 0, 0)
        test_record_3.status = "created"
        test_record_3.price = 1.0
        test_record_3.notes = ""
        test_record_3.user_id = user_id

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository, \
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockUserRepository.read_user_by_phone = AsyncMock(return_value=test_user)
            MockRecordRepository.read_record_by_user_id = AsyncMock(
                return_value=[test_record_1, test_record_2, test_record_3,]
            )

            result = await user_find_record(test_user_find, mock_session)

            assert isinstance(result, list)
            assert len(result) == 3
            assert isinstance(result[0], RecordResponse)
            assert isinstance(result[1], RecordResponse)
            assert isinstance(result[2], RecordResponse)

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user=test_user_find,
            )
            MockRecordRepository.read_record_by_user_id.assert_called_once_with(
                session=mock_session,
                user_id=user_id,
            )

    @pytest.mark.asyncio
    async def test_user_find_no_one_record(self):
        mock_session = AsyncMock()
        test_phone = "+79161234567"
        user_id = 1
        test_user_find = UserFind(phone_number=test_phone)
        test_user = MagicMock()
        test_user.id = user_id
        test_user.phone_number = test_phone

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository, \
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockUserRepository.read_user_by_phone = AsyncMock(return_value=test_user)
            MockRecordRepository.read_record_by_user_id = AsyncMock(
                return_value=[]
            )

            result = await user_find_record(test_user_find, mock_session)

            assert isinstance(result, list)
            assert len(result) == 0

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user=test_user_find,
            )
            MockRecordRepository.read_record_by_user_id.assert_called_once_with(
                session=mock_session,
                user_id=user_id,
            )
