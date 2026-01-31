import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from app.services.SpecializationService import get_specialization_by_id
from app.schemas.SpecializationService import SpecializationWithServicesResponse


@pytest.mark.asyncio
class TestGetSpecializationByIdService:

    async def test_get_specialization_by_id_success(self):
        mock_session = AsyncMock()
        mock_spec = AsyncMock()
        mock_spec.id = 1
        mock_spec.name = "Barber"
        mock_spec.services = []

        with patch("app.repositories.SpecializationRepository.read_specialization") as mock_repo:
            mock_repo.return_value = mock_spec

            result = await get_specialization_by_id(1, mock_session)
            mock_repo.assert_called_once_with(specialization_id=1, session=mock_session)
            assert isinstance(result, SpecializationWithServicesResponse)
            assert result.name == "Barber"
            assert result.id == 1

    async def test_get_specialization_by_id_not_found(self):
        mock_session = AsyncMock()
        with patch("app.repositories.SpecializationRepository.read_specialization") as mock_repo:
            mock_repo.return_value = None

            with pytest.raises(HTTPException) as exc:
                await get_specialization_by_id(999, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Specialization not found"
