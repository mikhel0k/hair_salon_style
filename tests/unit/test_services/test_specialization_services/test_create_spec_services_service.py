import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.SpecializationServicesService import create_spec_services
from app.schemas.SpecializationService import SpecializationServicesSchema


def _mock_specialization():
    return MagicMock()


@pytest.mark.asyncio
class TestCreateSpecServicesService:

    async def test_create_spec_services_success_add(self):
        mock_session = AsyncMock()
        data = SpecializationServicesSchema(specialization_id=1, services_id={1, 2})

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=_mock_specialization()), \
                patch("app.repositories.SpecializationServiceRepository.read_services_by_specialization", new_callable=AsyncMock) as mock_read, \
                patch("app.repositories.SpecializationServiceRepository.create_specialization_services") as mock_create:
            mock_read.return_value = []

            await create_spec_services(mock_session, data)

            mock_read.assert_called_once_with(specialization_id=1, session=mock_session)
            mock_create.assert_called_once()
            mock_session.commit.assert_called_once()

    async def test_create_spec_services_success_no_add_no_delete(self):
        mock_session = AsyncMock()
        data = SpecializationServicesSchema(specialization_id=1, services_id={1, 2})
        mock_s1 = MagicMock()
        mock_s1.id = 1
        mock_s2 = MagicMock()
        mock_s2.id = 2

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=_mock_specialization()), \
                patch("app.repositories.SpecializationServiceRepository.read_services_by_specialization", new_callable=AsyncMock) as mock_read:
            mock_read.return_value = [mock_s1, mock_s2]

            await create_spec_services(mock_session, data)

            mock_read.assert_called_once_with(specialization_id=1, session=mock_session)
            mock_session.commit.assert_called_once()

    async def test_create_spec_services_integrity_error_on_create(self):
        mock_session = AsyncMock()
        data = SpecializationServicesSchema(specialization_id=1, services_id={1})

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=_mock_specialization()), \
                patch("app.repositories.SpecializationServiceRepository.read_services_by_specialization", new_callable=AsyncMock) as mock_read, \
                patch("app.repositories.SpecializationServiceRepository.create_specialization_services") as mock_create:
            mock_read.return_value = []
            mock_create.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                await create_spec_services(mock_session, data)

            assert exc.value.status_code == 409
            assert "SpecializationServices" in exc.value.detail
            mock_session.rollback.assert_called_once()
