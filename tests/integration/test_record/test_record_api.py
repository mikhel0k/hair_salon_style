import pytest
from datetime import date
from httpx import AsyncClient
from starlette import status

WEEKDAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


@pytest.fixture
async def category_id(ac: AsyncClient, token):
    response = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def service_id(ac: AsyncClient, token, category_id):
    response = await ac.post(
        "/v1/service/",
        json={
            "name": "Haircut",
            "price": 500,
            "duration_minutes": 30,
            "category_id": category_id,
            "description": "Classic haircut",
        },
        headers=token,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def specialization_id(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


@pytest.fixture
async def master_id(ac: AsyncClient, token, specialization_id, service_id):
    await ac.put(
        "/v1/service/specialization/",
        json={"specialization_id": specialization_id, "services_id": [service_id]},
        headers=token,
    )
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
    mid = response.json()["id"]
    today = date.today()
    day_name = WEEKDAY_NAMES[today.weekday()]
    await ac.patch(
        f"/v1/schedule/{mid}/",
        json={f"{day_name}_start": "09:00:00", f"{day_name}_end": "18:00:00"},
        headers=token,
    )
    cell_resp = await ac.post(f"/v1/cell/{mid}/", headers=token)
    assert cell_resp.status_code == status.HTTP_201_CREATED
    return mid


@pytest.fixture
async def cell_id(ac: AsyncClient, master_id):
    today = date.today().isoformat()
    response = await ac.get(f"/v1/cell/?master_id={master_id}&date={today}")
    assert response.status_code == status.HTTP_200_OK
    cells = response.json()
    assert len(cells) > 0
    return cells[0]["id"]


@pytest.mark.asyncio
async def test_post_record_201(ac: AsyncClient, master_id, service_id, cell_id):
    payload = {
        "phone_number": "+79009009090",
        "master_id": master_id,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    response = await ac.post("/v1/record/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["master_id"] == master_id
    assert data["service_id"] == service_id
    assert data["cell_id"] == cell_id
    assert data["status"] == "CREATED"
    assert "id" in data


@pytest.mark.asyncio
async def test_post_record_409_master_not_provides(ac: AsyncClient, master_id, service_id, cell_id):
    p = {
        "phone_number": "+79009009090",
        "master_id": 99999,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    response = await ac.post("/v1/record/", json=p)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Master not provides" in response.json()["detail"]


@pytest.mark.asyncio
async def test_post_record_422_invalid_phone(ac: AsyncClient, master_id, service_id, cell_id):
    p = {
        "phone_number": "x",
        "master_id": master_id,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    response = await ac.post("/v1/record/", json=p)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_get_records_by_phone_200(ac: AsyncClient, master_id, service_id, cell_id):
    payload = {
        "phone_number": "+79001234567",
        "master_id": master_id,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    await ac.post("/v1/record/", json=payload)
    response = await ac.get("/v1/record/by-phone/+79001234567/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_records_by_phone_404(ac: AsyncClient):
    response = await ac.get("/v1/record/by-phone/+79999999999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_patch_record_404(ac: AsyncClient, token):
    response = await ac.patch(
        "/v1/record/99999/",
        json={"notes": "New note"},
        headers=token,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Record not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_put_record_status_cancelled_404(ac: AsyncClient):
    response = await ac.put("/v1/record/99999/status/cancelled/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Record not found"


@pytest.mark.asyncio
async def test_put_record_note_404(ac: AsyncClient, token):
    response = await ac.put(
        "/v1/record/99999/note/",
        json={"id": 99999, "notes": "Note"},
        headers=token,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Record not found"


@pytest.mark.asyncio
async def test_post_record_409_cell_already_occupied(ac: AsyncClient, master_id, service_id, cell_id):
    payload = {
        "phone_number": "+79001112233",
        "master_id": master_id,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    await ac.post("/v1/record/", json=payload)
    response = await ac.post("/v1/record/", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Cell already occupied" in response.json()["detail"]


@pytest.mark.asyncio
async def test_put_record_status_confirmed_401_not_master(ac: AsyncClient, token, master_id, service_id, cell_id):
    payload = {
        "phone_number": "+79003334455",
        "master_id": master_id,
        "service_id": service_id,
        "cell_id": cell_id,
        "notes": None,
    }
    create_resp = await ac.post("/v1/record/", json=payload)
    assert create_resp.status_code == status.HTTP_201_CREATED
    record_id = create_resp.json()["id"]
    response = await ac.put(
        f"/v1/record/{record_id}/status/confirmed/",
        headers=token,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
