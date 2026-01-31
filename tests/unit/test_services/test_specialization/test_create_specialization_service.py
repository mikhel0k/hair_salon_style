import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.SpecializationService import create_specialization
from app.schemas.Specialization import SpecializationCreate, SpecializationResponse


@pytest.mark.asyncio
class TestCreateSpecializationService:

    async def test_create_specialization_success(self):
        mock_session = AsyncMock()
        spec_in = SpecializationCreate(name="Barber")

        mock_spec_db = AsyncMock()
        mock_spec_db.id = 1
        mock_spec_db.name = "Barber"

        with patch("app.repositories.SpecializationRepository.create_specialization") as mock_repo:
            mock_repo.return_value = mock_spec_db

            result = await create_specialization(spec_in, mock_session)

            mock_repo.assert_called_once_with(specialization_data=spec_in, session=mock_session)
            assert isinstance(result, SpecializationResponse)
            assert result.name == "Barber"
            mock_session.commit.assert_called_once()

    async def test_create_specialization_integrity_error(self):
        mock_session = AsyncMock()
        spec_in = SpecializationCreate(name="Barber")

        with patch("app.repositories.SpecializationRepository.create_specialization") as mock_repo:
            mock_repo.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                await create_specialization(spec_in, mock_session)

            mock_repo.assert_called_once_with(specialization_data=spec_in, session=mock_session)
            assert exc.value.status_code == 409
            assert exc.value.detail == "Specialization with this data already exists"
            mock_session.rollback.assert_called_once()
