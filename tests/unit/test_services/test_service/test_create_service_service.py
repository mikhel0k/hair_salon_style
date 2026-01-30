import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.ServiceService import create_service
from app.schemas.Service import ServiceCreate, ServiceResponse


@pytest.mark.asyncio
class TestCreateServiceService:

    async def test_create_service_success(self):
        mock_session = AsyncMock()
        service_in = ServiceCreate(
            name="Haircut",
            price=500,
            duration_minutes=30,
            category_id=1,
            description="Desc",
        )

        mock_service_db = AsyncMock()
        mock_service_db.id = 1
        mock_service_db.name = "Haircut"
        mock_service_db.price = 500
        mock_service_db.duration_minutes = 30
        mock_service_db.category_id = 1
        mock_service_db.description = "Desc"

        with patch("app.repositories.ServiceRepository.create_service") as mock_repo:
            mock_repo.return_value = mock_service_db

            result = await create_service(service_in, mock_session)

            mock_repo.assert_called_once_with(service=service_in, session=mock_session)

            assert isinstance(result, ServiceResponse)
            assert result.name == "Haircut"
            assert result.price == 500
            mock_session.commit.assert_called_once()

    async def test_create_service_integrity_error(self):
        mock_session = AsyncMock()
        service_in = ServiceCreate(
            name="Haircut",
            price=500,
            duration_minutes=30,
            category_id=1,
            description="Desc",
        )

        with patch("app.repositories.ServiceRepository.create_service") as mock_repo:
            mock_repo.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                await create_service(service_in, mock_session)

            mock_repo.assert_called_once_with(service=service_in, session=mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Service with this data already exists"
            mock_session.rollback.assert_called_once()
