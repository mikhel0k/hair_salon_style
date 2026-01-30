import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.ServiceService import delete_service


@pytest.mark.asyncio
class TestDeleteServiceService:

    async def test_delete_service_success(self):
        mock_session = AsyncMock()
        service_id = 1

        mock_service_db = AsyncMock()
        mock_service_db.id = service_id

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=mock_service_db) as mock_read, \
                patch("app.repositories.ServiceRepository.delete_service", return_value=None) as mock_delete:
            await delete_service(service_id, mock_session)

            mock_read.assert_called_once_with(service_id=service_id, session=mock_session)
            mock_delete.assert_called_once_with(service=mock_service_db, session=mock_session)
            mock_session.commit.assert_called_once()

    async def test_delete_service_not_found(self):
        mock_session = AsyncMock()
        service_id = 999

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=None) as mock_read:
            with pytest.raises(HTTPException) as exc:
                await delete_service(service_id, mock_session)

            mock_read.assert_called_once_with(service_id=service_id, session=mock_session)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Service not found"
            mock_session.commit.assert_not_called()

    async def test_delete_service_integrity_error(self):
        mock_session = AsyncMock()
        service_id = 1
        mock_service_db = AsyncMock()

        with patch("app.repositories.ServiceRepository.read_service_by_id", return_value=mock_service_db), \
                patch("app.repositories.ServiceRepository.delete_service",
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await delete_service(service_id, mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Service with this data already exists"
            mock_session.rollback.assert_called_once()
