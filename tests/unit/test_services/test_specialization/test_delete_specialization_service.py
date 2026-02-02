import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from app.services.SpecializationService import delete_specialization


@pytest.mark.asyncio
class TestDeleteSpecializationService:

    async def test_delete_specialization_success(self):
        mock_session = AsyncMock()
        specialization_id = 1
        mock_spec = AsyncMock()
        mock_spec.id = specialization_id
        mock_spec.name = "Barber"

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=mock_spec), \
                patch("app.repositories.MasterRepository.count_masters_by_specialization_id", new_callable=AsyncMock, return_value=0), \
                patch("app.repositories.SpecializationServiceRepository.delete_all_by_specialization_id", new_callable=AsyncMock), \
                patch("app.repositories.SpecializationRepository.delete_specialization", new_callable=AsyncMock):
            await delete_specialization(specialization_id, mock_session)

            mock_session.commit.assert_called_once()

    async def test_delete_specialization_not_found(self):
        mock_session = AsyncMock()
        specialization_id = 999

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await delete_specialization(specialization_id, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Specialization not found"
            mock_session.commit.assert_not_called()

    async def test_delete_specialization_409_has_linked_masters(self):
        mock_session = AsyncMock()
        specialization_id = 1
        mock_spec = AsyncMock()
        mock_spec.id = specialization_id
        mock_spec.name = "Barber"

        with patch("app.repositories.SpecializationRepository.read_specialization", new_callable=AsyncMock, return_value=mock_spec), \
                patch("app.repositories.MasterRepository.count_masters_by_specialization_id", new_callable=AsyncMock, return_value=2):
            with pytest.raises(HTTPException) as exc:
                await delete_specialization(specialization_id, mock_session)

            assert exc.value.status_code == 409
            assert "linked masters" in exc.value.detail
            mock_session.commit.assert_not_called()
