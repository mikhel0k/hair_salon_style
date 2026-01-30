import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def category_id(ac: AsyncClient, token):
    response = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


def _service_payload(category_id, name="Haircut", price=500, duration_minutes=30, description="Desc"):
    return {"name": name, "price": price, "duration_minutes": duration_minutes, "category_id": category_id, "description": description}


_NAMES_BY_COUNT = ["Haircut", "Beard trim", "Coloring"]


@pytest.mark.parametrize(
    "count",
    [0, 1, 3],
)
@pytest.mark.asyncio
async def test_get_services_200(ac: AsyncClient, token, category_id, count):
    for i in range(count):
        p = _service_payload(category_id, name=_NAMES_BY_COUNT[i])
        response = await ac.post("/v1/service/", json=p, headers=token)
        assert response.status_code == status.HTTP_201_CREATED

    response = await ac.get("/v1/service/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count


@pytest.mark.asyncio
async def test_get_services_by_category_200(ac: AsyncClient, token, category_id):
    p1 = _service_payload(category_id, "Haircut")
    p2 = _service_payload(category_id, "Beard trim")
    for p in (p1, p2):
        response = await ac.post("/v1/service/", json=p, headers=token)
        assert response.status_code == status.HTTP_201_CREATED

    response = await ac.get(f"/v1/service/{category_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_services_by_category_empty_200(ac: AsyncClient, token, category_id):
    response = await ac.get(f"/v1/service/{category_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
