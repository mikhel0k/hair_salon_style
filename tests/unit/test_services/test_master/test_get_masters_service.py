import pytest
from unittest.mock import AsyncMock, patch

from app.services.MasterService import get_masters
from app.schemas.Master import MasterFullResponse, AllowedMasterStatuses


def _master_obj(mid, name, spec_id=1, spec_name="Barber"):
    spec = type("Spec", (), {"id": spec_id, "name": spec_name})()
    return type("Master", (), {
        "id": mid,
        "name": name,
        "specialization_id": spec_id,
        "phone": "+79009009090",
        "email": "petr@mail.ru",
        "status": AllowedMasterStatuses.ACTIVE,
        "specialization": spec,
    })()


@pytest.mark.asyncio
class TestGetMastersService:

    async def test_get_masters_success(self):
        mock_session = AsyncMock()
        mock_m1 = _master_obj(1, "Petr")
        mock_m2 = _master_obj(2, "Ivan")

        with patch("app.repositories.MasterRepository.read_masters", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = [mock_m1, mock_m2]

            result = await get_masters(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)
            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(r, MasterFullResponse) for r in result)

    async def test_get_masters_empty(self):
        mock_session = AsyncMock()
        with patch("app.repositories.MasterRepository.read_masters", new_callable=AsyncMock) as mock_repo:
            mock_repo.return_value = []
            result = await get_masters(mock_session, 0, 99)
            assert isinstance(result, list)
            assert len(result) == 0
