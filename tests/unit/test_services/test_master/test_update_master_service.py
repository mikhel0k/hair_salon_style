import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.MasterService import update_master
from app.schemas.Master import MasterUpdate, MasterResponse


@pytest.mark.asyncio
class TestUpdateMasterService:

    async def test_update_master_success(self):
        mock_session = AsyncMock()
        master_id = 1
        update_data = MasterUpdate(name="New Name")

        mock_master_db = AsyncMock()
        mock_master_db.id = master_id
        mock_master_db.name = "New Name"
        mock_master_db.specialization_id = 1
        mock_master_db.phone = "+79009009090"
        mock_master_db.email = "petr@mail.ru"
        mock_master_db.status = "ACTIVE"

        with patch("app.repositories.MasterRepository.read_master", new_callable=AsyncMock, return_value=mock_master_db) as mock_read, \
                patch("app.repositories.MasterRepository.update_master", new_callable=AsyncMock, return_value=mock_master_db) as mock_update:
            result = await update_master(master_id, update_data, mock_session)

            mock_read.assert_called_once_with(master_id=master_id, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, MasterResponse)
            assert result.name == "New Name"

    async def test_update_master_not_found(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.read_master", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await update_master(999, MasterUpdate(name="Val"), mock_session)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Master not found"

    async def test_update_master_integrity_error(self):
        mock_session = AsyncMock()
        mock_master_db = AsyncMock()
        with patch("app.repositories.MasterRepository.read_master", new_callable=AsyncMock, return_value=mock_master_db), \
                patch("app.repositories.MasterRepository.update_master", new_callable=AsyncMock,
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_master(1, MasterUpdate(name="Dup"), mock_session)
            assert exc.value.status_code == 409
            assert exc.value.detail == "Master with this data already exists"
            mock_session.rollback.assert_called_once()
