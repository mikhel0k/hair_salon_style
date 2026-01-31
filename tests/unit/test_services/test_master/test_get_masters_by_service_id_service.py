import pytest
from unittest.mock import AsyncMock, patch

from app.services.MasterService import get_masters_by_service_id
from app.schemas.Master import MasterResponse, AllowedMasterStatuses


def _master_response_obj(mid=1, name="Petr", spec_id=1):
    return type("Master", (), {
        "id": mid,
        "name": name,
        "specialization_id": spec_id,
        "phone": "+79009009090",
        "email": "petr@mail.ru",
        "status": AllowedMasterStatuses.ACTIVE,
    })()


@pytest.mark.asyncio
class TestGetMastersByServiceIdService:

    async def test_get_masters_by_service_id_success(self):
        mock_session = AsyncMock()
        mock_m = _master_response_obj(1, "Petr")

        with patch("app.repositories.MasterRepository.read_masters_by_service_id", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = [mock_m]

            result = await get_masters_by_service_id(1, mock_session, 0, 99)
            mock_repo.assert_called_once_with(
                service_id=1, session=mock_session, skip=0, limit=99
            )
            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], MasterResponse)

    async def test_get_masters_by_service_id_empty(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.read_masters_by_service_id", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = []
            result = await get_masters_by_service_id(1, mock_session, 0, 99)
            assert isinstance(result, list)
            assert len(result) == 0
