import pytest
from unittest.mock import AsyncMock, patch

from app.services.ServiceService import get_services
from app.schemas.Service import ServiceResponse


@pytest.mark.asyncio
class TestGetServicesService:

    async def test_get_services_success(self):
        mock_session = AsyncMock()

        mock_s1 = AsyncMock()
        mock_s1.id = 1
        mock_s1.name = "Haircut"
        mock_s1.price = 500
        mock_s1.duration_minutes = 30
        mock_s1.category_id = 1
        mock_s1.description = "Desc"

        mock_s2 = AsyncMock()
        mock_s2.id = 2
        mock_s2.name = "Beard"
        mock_s2.price = 300
        mock_s2.duration_minutes = 15
        mock_s2.category_id = 1
        mock_s2.description = "Desc"

        with patch("app.repositories.ServiceRepository.read_services") as mock_repo:
            mock_repo.return_value = [mock_s1, mock_s2]

            result = await get_services(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(r, ServiceResponse) for r in result)
            assert result[0].name == "Haircut"
            assert result[0].id == 1
            assert result[1].name == "Beard"
            assert result[1].id == 2

    async def test_get_services_empty(self):
        mock_session = AsyncMock()

        with patch("app.repositories.ServiceRepository.read_services") as mock_repo:
            mock_repo.return_value = []

            result = await get_services(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)

            assert isinstance(result, list)
            assert len(result) == 0
