import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def category_id(ac: AsyncClient, token):
    response = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def service_id(ac: AsyncClient, token, category_id):
    response = await ac.post(
        "/v1/service/",
        json={"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": category_id, "description": "D"},
        headers=token,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.mark.parametrize(
    "patch_payload",
    [
        {"name": "New name"},
        {"price": 600},
        {"duration_minutes": 45},
        {"description": "New desc"},
        {"name": "Updated", "price": 700, "duration_minutes": 60, "description": "Full update"},
    ],
)
@pytest.mark.asyncio
async def test_patch_service_202(ac: AsyncClient, token, service_id, patch_payload):
    response = await ac.patch(f"/v1/service/{service_id}/", json=patch_payload, headers=token)
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    for key, value in patch_payload.items():
        if key == "name":
            assert data[key] == value.strip().title()
        elif key == "price":
            raw = data[key]
            assert (raw == value or float(raw) == value)
        else:
            assert data[key] == value


@pytest.mark.asyncio
async def test_patch_service_404(ac: AsyncClient, token):
    response = await ac.patch("/v1/service/99999/", json={"name": "Valid name"}, headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Service not found"


@pytest.mark.asyncio
async def test_patch_service_401(ac: AsyncClient, service_id):
    response = await ac.patch(f"/v1/service/{service_id}/", json={"name": "Valid name"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
