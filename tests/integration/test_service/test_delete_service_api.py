import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def category_id(ac: AsyncClient, token):
    response = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.mark.parametrize(
    "payload",
    [
        [{"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "D"}],
        [
            {"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "D"},
            {"name": "Beard", "price": 300, "duration_minutes": 15, "category_id": 1, "description": "D"},
        ],
    ],
)
@pytest.mark.asyncio
async def test_delete_service_204(ac: AsyncClient, payload, token, category_id):
    created_ids = []
    for p in payload:
        full = {**p, "category_id": category_id}
        res = await ac.post("/v1/service/", json=full, headers=token)
        assert res.status_code == status.HTTP_201_CREATED
        created_ids.append(res.json()["id"])

    for sid in created_ids:
        response = await ac.delete(f"/v1/service/{sid}/", headers=token)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_service_404(ac: AsyncClient, token):
    response = await ac.delete("/v1/service/99999/", headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Service not found"


@pytest.mark.asyncio
async def test_delete_service_401(ac: AsyncClient, token, category_id):
    res = await ac.post(
        "/v1/service/",
        json={"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": category_id, "description": "D"},
        headers=token,
    )
    assert res.status_code == status.HTTP_201_CREATED
    sid = res.json()["id"]
    response = await ac.delete(f"/v1/service/{sid}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
