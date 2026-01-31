import pytest
from unittest.mock import AsyncMock, patch

from app.services.SpecializationService import get_specializations
from app.schemas.Specialization import SpecializationResponse


@pytest.mark.asyncio
class TestGetSpecializationsService:

    async def test_get_specializations_success(self):
        mock_session = AsyncMock()
        mock_s1 = AsyncMock()
        mock_s1.id = 1
        mock_s1.name = "Barber"
        mock_s2 = AsyncMock()
        mock_s2.id = 2
        mock_s2.name = "Manicure"

        with patch("app.repositories.SpecializationRepository.read_specializations") as mock_repo:
            mock_repo.return_value = [mock_s1, mock_s2]

            result = await get_specializations(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)
            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(r, SpecializationResponse) for r in result)
            assert result[0].name == "Barber"
            assert result[1].name == "Manicure"

    async def test_get_specializations_empty(self):
        mock_session = AsyncMock()
        with patch("app.repositories.SpecializationRepository.read_specializations") as mock_repo:
            mock_repo.return_value = []
            result = await get_specializations(mock_session, 0, 99)
            assert isinstance(result, list)
            assert len(result) == 0
