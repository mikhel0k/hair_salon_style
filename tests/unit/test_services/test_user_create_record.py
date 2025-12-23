from unittest.mock import MagicMock, patch, AsyncMock
from datetime import date, time
import pytest

from app.services.RecordForUser import user_create_record
from app.schemas import MakeRecord, RecordResponse, UserFind, UserCreate, RecordCreate


class TestUserCreateRecord:
    @pytest.mark.asyncio
    async def test_create_record_and_new_user(self):
        mock_session = MagicMock()

        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock()
        mock_context.__aexit__ = AsyncMock()

        mock_session.begin.return_value = mock_context

        phone_number = "+79161234567"
        date_record = date.today()
        time_record = time(hour=23, minute=59, second=59)
        notes = "I want to drink beer while getting a haircut"
        user_id = 1

        make_record = MakeRecord(
            phone_number=phone_number,
            date=date_record,
            time=time_record,
            master_id=1,
            service_id=1,
            notes=notes,
        )

        test_user = MagicMock()
        test_user.id = user_id
        test_user.phone_number = phone_number

        test_record = MagicMock()
        test_record.id = 1
        test_record.date = date_record
        test_record.time = time_record
        test_record.status = "created"
        test_record.price = 0
        test_record.notes = notes
        test_record.user_id = user_id
        test_record.master_id = 1
        test_record.service_id = 1

        test_user_find = UserFind(phone_number=phone_number)
        test_user_create = UserCreate(phone_number=phone_number)
        test_record_create = RecordCreate(
            user_id=user_id,
            date=date_record,
            time=time_record,
            master_id=1,
            service_id=1,
            notes=notes,
        )

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository, \
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:

            MockUserRepository.read_user_by_phone = AsyncMock(return_value=None)
            MockUserRepository.create_user = AsyncMock(return_value=test_user)
            MockRecordRepository.create_record = AsyncMock(return_value=test_record)

            result = await user_create_record(
                record=make_record,
                session=mock_session,
            )

            assert isinstance(result, RecordResponse)

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user = test_user_find,
            )

            MockUserRepository.create_user.assert_called_once_with(
                session=mock_session,
                user = test_user_create,
            )

            MockRecordRepository.create_record.assert_called_once_with(
                session=mock_session,
                record = test_record_create,
            )

            assert result.id == 1
            assert result.date == date_record
            assert result.time == time_record
            assert result.status == "created"
            assert result.price == 0
            assert result.notes == notes
            assert result.user_id == user_id
            assert result.master_id == 1
            assert result.service_id == 1

    @pytest.mark.asyncio
    async def test_create_record_and_old_user(self):
        mock_session = MagicMock()

        mock_context = MagicMock()
        mock_context.__aenter__ = AsyncMock()
        mock_context.__aexit__ = AsyncMock()

        mock_session.begin.return_value = mock_context

        phone_number = "+79161234567"
        date_record = date.today()
        time_record = time(hour=23, minute=59, second=59)
        notes = "I want to drink beer while getting a haircut"
        user_id = 1

        make_record = MakeRecord(
            phone_number=phone_number,
            date=date_record,
            time=time_record,
            master_id=1,
            service_id=1,
            notes=notes,
        )

        test_user = MagicMock()
        test_user.id = user_id
        test_user.phone_number = phone_number

        test_record = MagicMock()
        test_record.id = 1
        test_record.date = date_record
        test_record.time = time_record
        test_record.status = "created"
        test_record.price = 0
        test_record.notes = notes
        test_record.user_id = user_id
        test_record.master_id = 1
        test_record.service_id = 1

        test_user_find = UserFind(phone_number=phone_number)
        test_record_create = RecordCreate(
            user_id=user_id,
            date=date_record,
            time=time_record,
            master_id=1,
            service_id=1,
            notes=notes,
        )

        with patch('app.services.RecordForUser.UserRepository') as MockUserRepository, \
                patch('app.services.RecordForUser.RecordRepository') as MockRecordRepository:
            MockUserRepository.read_user_by_phone = AsyncMock(return_value=test_user)
            MockUserRepository.create_user = AsyncMock(return_value=test_user)
            MockRecordRepository.create_record = AsyncMock(return_value=test_record)

            result = await user_create_record(
                record=make_record,
                session=mock_session,
            )

            assert isinstance(result, RecordResponse)

            MockUserRepository.read_user_by_phone.assert_called_once_with(
                session=mock_session,
                user=test_user_find,
            )

            MockUserRepository.create_user.assert_not_called()

            MockRecordRepository.create_record.assert_called_once_with(
                session=mock_session,
                record=test_record_create,
            )

            assert result.id == 1
            assert result.date == date_record
            assert result.time == time_record
            assert result.status == "created"
            assert result.price == 0
            assert result.notes == notes
            assert result.user_id == user_id
            assert result.master_id == 1
            assert result.service_id == 1
