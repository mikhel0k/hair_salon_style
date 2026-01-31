import pytest
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


@pytest.mark.asyncio
async def test_get_schedule_by_master_id_for_admin_200(ac: AsyncClient, token, master_id):
    response = await ac.get(f"/v1/schedule/{master_id}/", headers=token)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == master_id
    assert data["master_id"] == master_id


@pytest.mark.asyncio
async def test_get_schedule_by_master_id_404(ac: AsyncClient, token):
    response = await ac.get("/v1/schedule/99999/", headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Schedule not found"


@pytest.mark.asyncio
async def test_get_schedule_401(ac: AsyncClient, master_id):
    response = await ac.get(f"/v1/schedule/{master_id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_patch_schedule_for_admin_202(ac: AsyncClient, token, master_id):
    payload = {
        "monday_start": "09:00:00",
        "monday_end": "18:00:00",
    }
    response = await ac.patch(f"/v1/schedule/{master_id}/", json=payload, headers=token)
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert data["id"] == master_id
    assert data["monday_start"] == "09:00:00"
    assert data["monday_end"] == "18:00:00"


@pytest.mark.asyncio
async def test_patch_schedule_404(ac: AsyncClient, token):
    response = await ac.patch(
        "/v1/schedule/99999/",
        json={"monday_start": "09:00:00", "monday_end": "18:00:00"},
        headers=token,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Schedule not found"
