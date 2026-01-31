import pytest
from httpx import AsyncClient
from starlette import status

from tests.integration.test_master.conftest import master_payload


@pytest.fixture
async def master_id(ac: AsyncClient, token, specialization_id):
    p = master_payload(specialization_id)
    response = await ac.post("/v1/master/", json=p, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.mark.parametrize(
    "patch_payload",
    [
        {"name": "New name"},
        {"status": "VACATION"},
        {"email": "new@mail.ru"},
    ],
)
@pytest.mark.asyncio
async def test_patch_master_200(ac: AsyncClient, token, master_id, patch_payload):
    response = await ac.patch(f"/v1/master/{master_id}/", json=patch_payload, headers=token)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for key, value in patch_payload.items():
        if key == "name":
            assert data[key] == value.strip().title()
        else:
            assert data[key] == value


@pytest.mark.asyncio
async def test_patch_master_404(ac: AsyncClient, token):
    response = await ac.patch("/v1/master/99999/", json={"name": "Valid name"}, headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Master not found"


@pytest.mark.asyncio
async def test_patch_master_401(ac: AsyncClient, master_id):
    response = await ac.patch(f"/v1/master/{master_id}/", json={"name": "Valid name"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
