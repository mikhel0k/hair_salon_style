import pytest
from httpx import AsyncClient
from starlette import status


_NAMES = ["Barber", "Manicure", "Stylist"]


@pytest.mark.parametrize(
    "count",
    [0, 1, 3],
)
@pytest.mark.asyncio
async def test_get_specializations_200(ac: AsyncClient, token, count):
    for i in range(count):
        response = await ac.post("/v1/specialization/", json={"name": _NAMES[i]}, headers=token)
        assert response.status_code == status.HTTP_201_CREATED

    response = await ac.get("/v1/specialization/", headers=token)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count


@pytest.mark.asyncio
async def test_get_specialization_by_id_200(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    sid = response.json()["id"]
    response = await ac.get(f"/v1/specialization/{sid}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == sid
    assert response.json()["name"] == "Barber"


@pytest.mark.asyncio
async def test_get_specialization_by_id_404(ac: AsyncClient):
    response = await ac.get("/v1/specialization/99999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Specialization not found"


@pytest.mark.asyncio
async def test_get_specializations_401(ac: AsyncClient):
    response = await ac.get("/v1/specialization/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
