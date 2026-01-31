import pytest
from httpx import AsyncClient
from starlette import status

from tests.integration.test_master.conftest import master_payload


@pytest.mark.parametrize(
    "payload",
    [
        [{"name": "Petr", "phone": "+79009009090", "email": "petr@mail.ru", "status": "ACTIVE", "specialization_id": 1}],
        [
            {"name": "Petr", "phone": "+79009009090", "email": "petr@mail.ru", "status": "ACTIVE", "specialization_id": 1},
            {"name": "Ivan", "phone": "89005553535", "email": "ivan@gmail.com", "status": "VACATION", "specialization_id": 1},
        ],
    ],
)
@pytest.mark.asyncio
async def test_post_master_201(ac: AsyncClient, payload, token, specialization_id):
    for i in range(len(payload)):
        p = {**payload[i], "specialization_id": specialization_id}
        response = await ac.post("/v1/master/", json=p, headers=token)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == p["name"].title()
        assert "id" in response.json()
        assert response.json()["specialization_id"] == specialization_id


@pytest.mark.parametrize(
    "payload, message_part",
    [
        ({"name": "ab", "phone": "+79009009090", "email": "petr@mail.ru", "status": "ACTIVE", "specialization_id": 1}, "at least 3"),
        ({"name": "Petr", "phone": "123", "email": "petr@mail.ru", "status": "ACTIVE", "specialization_id": 1}, "Invalid phone"),
        ({"name": "Petr", "phone": "+79009009090", "email": "bad", "status": "ACTIVE", "specialization_id": 1}, "valid"),
        ({"name": "Petr", "phone": "+79009009090", "email": "petr@mail.ru", "status": "ACTIVE", "specialization_id": -1}, "greater than or equal to 1"),
    ],
)
@pytest.mark.asyncio
async def test_post_master_422(ac: AsyncClient, payload, message_part, token, specialization_id):
    p = {**payload}
    if payload.get("specialization_id") == 1:
        p["specialization_id"] = specialization_id
    if payload.get("specialization_id") == -1:
        p["specialization_id"] = -1
    response = await ac.post("/v1/master/", json=p, headers=token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = response.json()["detail"]
    if isinstance(detail, list):
        detail_msg = " ".join(str(d.get("msg", "")) for d in detail)
    else:
        detail_msg = str(detail)
    assert message_part in detail_msg


@pytest.mark.asyncio
async def test_post_master_409(ac: AsyncClient, token, specialization_id):
    p = master_payload(specialization_id)
    response = await ac.post("/v1/master/", json=p, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    response = await ac.post("/v1/master/", json=p, headers=token)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Master with this data already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_post_master_401(ac: AsyncClient, specialization_id):
    p = master_payload(specialization_id)
    response = await ac.post("/v1/master/", json=p)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
