import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def category_id(ac: AsyncClient, token):
    """Создаёт категорию и возвращает её id для использования в тестах услуг."""
    response = await ac.post("/v1/category/", json={"name": "Haircut"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


SERVICE_PAYLOAD = {
    "name": "Men's haircut",
    "price": 500,
    "duration_minutes": 30,
    "category_id": 1,  # подставится через category_id
    "description": "Classic men's haircut",
}


@pytest.mark.parametrize(
    "payload",
    [
        [
            {"name": "Mens haircut", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "Desc"},
        ],
        [
            {"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "Desc"},
            {"name": "Beard trim", "price": 300, "duration_minutes": 15, "category_id": 1, "description": "Desc"},
            {"name": "  Coloring  ", "price": 1000, "duration_minutes": 60, "category_id": 1, "description": "Desc"},
        ],
    ],
)
@pytest.mark.asyncio
async def test_post_service_201(ac: AsyncClient, payload, token, category_id):
    for i in range(len(payload)):
        p = {**payload[i], "category_id": category_id}
        response = await ac.post("/v1/service/", json=p, headers=token)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == p["name"].strip().title()
        raw_price = response.json()["price"]
        assert (raw_price == p["price"] or float(raw_price) == float(p["price"]))
        assert response.json()["duration_minutes"] == p["duration_minutes"]
        assert response.json()["category_id"] == category_id
        assert "id" in response.json()


@pytest.mark.parametrize(
    "payload, message",
    [
        ({"name": "123", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "D"}, "Value error, Invalid character"),
        ({"name": "ab", "price": 500, "duration_minutes": 30, "category_id": 1, "description": "D"}, "String should have at least 3 characters"),
        ({"name": "Haircut", "price": 0, "duration_minutes": 30, "category_id": 1, "description": "D"}, "greater than or equal to 1"),
        ({"name": "Haircut", "price": 500, "duration_minutes": 5, "category_id": 1, "description": "D"}, "greater than or equal to 10"),
        ({"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": 0, "description": "D"}, "greater than or equal to 1"),
        ({"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": 1, "description": 1}, "Input should be a valid string"),
    ],
)
@pytest.mark.asyncio
async def test_post_service_422(ac: AsyncClient, payload, message, token, category_id):
    p = {**payload}
    if payload.get("category_id") == 1:
        p["category_id"] = category_id
    response = await ac.post("/v1/service/", json=p, headers=token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert message in response.json()["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_post_service_409(ac: AsyncClient, token, category_id):
    p = {"name": "Unique cut", "price": 500, "duration_minutes": 30, "category_id": category_id, "description": "D"}
    response = await ac.post("/v1/service/", json=p, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    response = await ac.post("/v1/service/", json=p, headers=token)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Service with this data already exists"


@pytest.mark.asyncio
async def test_post_service_401(ac: AsyncClient, category_id):
    payload = {"name": "Haircut", "price": 500, "duration_minutes": 30, "category_id": category_id, "description": "D"}
    response = await ac.post("/v1/service/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
