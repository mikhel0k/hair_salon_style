import pytest
from unittest.mock import AsyncMock, patch

from app.services.ServiceService import get_services_by_category_id
from app.schemas.Service import ServiceResponse


@pytest.mark.asyncio
class TestGetServicesByCategoryIdService:

    async def test_get_services_by_category_id_success(self):
        mock_session = AsyncMock()
        category_id = 1

        mock_s1 = AsyncMock()
        mock_s1.id = 1
        mock_s1.name = "Haircut"
        mock_s1.price = 500
        mock_s1.duration_minutes = 30
        mock_s1.category_id = category_id
        mock_s1.description = "Desc"

        with patch("app.repositories.ServiceRepository.read_services_by_category_id") as mock_repo:
            mock_repo.return_value = [mock_s1]

            result = await get_services_by_category_id(category_id, mock_session, 0, 99)
            mock_repo.assert_called_once_with(
                category_id=category_id, session=mock_session, skip=0, limit=99
            )

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], ServiceResponse)
            assert result[0].name == "Haircut"
            assert result[0].category_id == category_id

    async def test_get_services_by_category_id_empty(self):
        mock_session = AsyncMock()
        category_id = 1

        with patch("app.repositories.ServiceRepository.read_services_by_category_id") as mock_repo:
            mock_repo.return_value = []

            result = await get_services_by_category_id(category_id, mock_session, 0, 99)
            mock_repo.assert_called_once_with(
                category_id=category_id, session=mock_session, skip=0, limit=99
            )

            assert isinstance(result, list)
            assert len(result) == 0
