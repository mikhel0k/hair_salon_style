import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.ServiceService import update_service
from app.schemas.Service import ServiceUpdate, ServiceResponse


@pytest.mark.asyncio
class TestUpdateServiceService:

    async def test_update_service_success(self):
        mock_session = AsyncMock()
        service_id = 1
        update_data = ServiceUpdate(name="New name")

        mock_service_db = AsyncMock()
        mock_service_db.id = service_id
        mock_service_db.name = "New name"
        mock_service_db.price = 500
        mock_service_db.duration_minutes = 30
        mock_service_db.category_id = 1
        mock_service_db.description = "Desc"

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=mock_service_db) as mock_read, \
                patch("app.repositories.ServiceRepository.update_service", return_value=mock_service_db) as mock_update:
            result = await update_service(service_id, update_data, mock_session)

            mock_read.assert_called_once_with(service_id=service_id, session=mock_session)
            mock_update.assert_called_once()
            mock_session.commit.assert_called_once()
            assert isinstance(result, ServiceResponse)
            assert result.name == "New Name"  # name_validator applies .title()

    async def test_update_service_not_found(self):
        mock_session = AsyncMock()
        service_id = 999
        update_data = ServiceUpdate(name="New name")

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=None) as mock_read:
            with pytest.raises(HTTPException) as exc:
                await update_service(service_id, update_data, mock_session)

            mock_read.assert_called_once_with(service_id=service_id, session=mock_session)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Service not found"
            mock_session.commit.assert_not_called()

    async def test_update_service_integrity_error(self):
        mock_session = AsyncMock()
        service_id = 1
        update_data = ServiceUpdate(name="Duplicate name")
        mock_service_db = AsyncMock()

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=mock_service_db), \
                patch("app.repositories.ServiceRepository.update_service",
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await update_service(service_id, update_data, mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Service with this data already exists"
            mock_session.rollback.assert_called_once()
