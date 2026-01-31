import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def specialization_id(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def service_ids(ac: AsyncClient, token):
    cat = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert cat.status_code == status.HTTP_201_CREATED
    cat_id = cat.json()["id"]
    s1 = await ac.post(
        "/v1/service/",
        json={"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": cat_id, "description": "D"},
        headers=token,
    )
    assert s1.status_code == status.HTTP_201_CREATED
    s2 = await ac.post(
        "/v1/service/",
        json={"name": "Beard trim", "price": 300, "duration_minutes": 15, "category_id": cat_id, "description": "D"},
        headers=token,
    )
    assert s2.status_code == status.HTTP_201_CREATED
    return [s1.json()["id"], s2.json()["id"]]


@pytest.mark.asyncio
async def test_put_specialization_service_202(ac: AsyncClient, token, specialization_id, service_ids):
    payload = {"specialization_id": specialization_id, "services_id": service_ids}
    response = await ac.put("/v1/service/specialization/", json=payload, headers=token)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == {"status": "success"}


@pytest.mark.asyncio
async def test_put_specialization_service_401(ac: AsyncClient, specialization_id, service_ids):
    payload = {"specialization_id": specialization_id, "services_id": service_ids}
    response = await ac.put("/v1/service/specialization/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_put_specialization_service_422(ac: AsyncClient, token):
    payload = {"specialization_id": 0, "services_id": [1]}
    response = await ac.put("/v1/service/specialization/", json=payload, headers=token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
