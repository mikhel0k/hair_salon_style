import pytest
from datetime import date
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def specialization_id(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def master_id(ac: AsyncClient, token, specialization_id):
    response = await ac.post(
        "/v1/master/",
        json={
            "specialization_id": specialization_id,
            "name": "Petr",
            "phone": "+79009009090",
            "email": "petr@mail.ru",
            "status": "ACTIVE",
        },
        headers=token,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def master_with_schedule(ac: AsyncClient, token, master_id):
    payload = {
        "monday_start": "09:00:00",
        "monday_end": "18:00:00",
        "tuesday_start": "09:00:00",
        "tuesday_end": "18:00:00",
    }
    response = await ac.patch(f"/v1/schedule/{master_id}/", json=payload, headers=token)
    assert response.status_code == status.HTTP_202_ACCEPTED
    return master_id


@pytest.mark.asyncio
async def test_post_cells_201(ac: AsyncClient, token, master_with_schedule):
    response = await ac.post(f"/v1/cell/{master_with_schedule}/", headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"status": "success"}


@pytest.mark.asyncio
async def test_post_cells_404(ac: AsyncClient, token):
    response = await ac.post("/v1/cell/99999/", headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_post_cells_401(ac: AsyncClient, master_with_schedule):
    response = await ac.post(f"/v1/cell/{master_with_schedule}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_get_cells_200(ac: AsyncClient, token, master_with_schedule):
    await ac.post(f"/v1/cell/{master_with_schedule}/", headers=token)
    today = date.today().isoformat()
    response = await ac.get(f"/v1/cell/?master_id={master_with_schedule}&date={today}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
