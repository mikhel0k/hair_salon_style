import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.MasterService import create_master
from app.schemas.Master import MasterCreate, MasterResponse


@pytest.mark.asyncio
class TestCreateMasterService:

    async def test_create_master_success(self):
        mock_session = AsyncMock()
        master_in = MasterCreate(
            specialization_id=1,
            name="Petr",
            phone="+79009009090",
            email="petr@mail.ru",
            status="ACTIVE",
        )

        mock_master_db = AsyncMock()
        mock_master_db.id = 1
        mock_master_db.name = "Petr"
        mock_master_db.specialization_id = 1
        mock_master_db.phone = "+79009009090"
        mock_master_db.email = "petr@mail.ru"
        mock_master_db.status = "ACTIVE"

        with patch("app.repositories.MasterRepository.create_master") as mock_repo, \
                patch("app.repositories.ScheduleRepository.create_schedule") as mock_schedule:
            mock_repo.return_value = mock_master_db

            result = await create_master(master_in, mock_session)

            mock_repo.assert_called_once()
            mock_schedule.assert_called_once()
            assert isinstance(result, MasterResponse)
            assert result.name == "Petr"
            mock_session.commit.assert_called_once()

    async def test_create_master_integrity_error(self):
        mock_session = AsyncMock()
        master_in = MasterCreate(
            specialization_id=1,
            name="Petr",
            phone="+79009009090",
            email="petr@mail.ru",
            status="ACTIVE",
        )

        with patch("app.repositories.MasterRepository.create_master") as mock_repo:
            mock_repo.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                await create_master(master_in, mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Master with this data already exists"
            mock_session.rollback.assert_called_once()
