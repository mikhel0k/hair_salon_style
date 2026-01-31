import pytest
from httpx import AsyncClient
from starlette import status

from tests.integration.test_master.conftest import master_payload


@pytest.mark.parametrize(
    "count",
    [0, 1, 2],
)
@pytest.mark.asyncio
async def test_get_masters_200(ac: AsyncClient, token, specialization_id, count):
    names = ["Petr", "Ivan"]
    for i in range(count):
        p = master_payload(specialization_id, name=names[i], email=f"user{i}@mail.ru")
        response = await ac.post("/v1/master/", json=p, headers=token)
        assert response.status_code == status.HTTP_201_CREATED

    response = await ac.get("/v1/master/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count


@pytest.mark.asyncio
async def test_get_masters_by_service_id_200(ac: AsyncClient, token, specialization_id):
    p = master_payload(specialization_id)
    response = await ac.post("/v1/master/", json=p, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    master_id = response.json()["id"]
    response = await ac.get("/v1/master/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1
