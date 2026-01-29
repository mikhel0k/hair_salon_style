import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.parametrize(
    "payload",
    [
        [{"name": "Haircut"},],
        [
            {"name": "Haircut"},
            {"name": "manicure"},
            {"name": "lamination    "},
            {"name": "   coloring"},
        ]
    ]
)
@pytest.mark.asyncio
async def test_post_category_201(ac: AsyncClient, payload, token):
    for i in range(0, len(payload)):
        response = await ac.post("/v1/category/", json=payload[i], headers=token)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == payload[i]['name'].strip().title()
        assert "id" in response.json()


@pytest.mark.parametrize(
    "payload, message",
    [
        ({"name": "123"}, "Value error, Invalid character"),
        ({"name": "a" * 2}, "String should have at least 3 characters"),
        ({"name": "a" * 61}, "String should have at most 60 characters"),
        ({"name": 1}, "Input should be a valid string"),
        ({"name": True}, "Input should be a valid string"),
        ({"name": "Haircut?"}, "Value error, Invalid character"),
    ]
)
@pytest.mark.asyncio
async def test_post_category_422(ac: AsyncClient, payload, message, token):
    response = await ac.post("/v1/category/", json=payload, headers=token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == message


@pytest.mark.parametrize(
    "payload, data",
    [
        ([{"name": "Haircut"},], {"name": "Haircut"},),
        ([{"name": "Haircut"}, {"name": "manicure"}], {"name": "Haircut"})
    ]
)
@pytest.mark.asyncio
async def test_post_category_409(ac: AsyncClient, payload, data, token):
    for i in range(0, len(payload)):
        response = await ac.post("/v1/category/", json=payload[i], headers=token)
        assert response.status_code == status.HTTP_201_CREATED

    response = await ac.post("/v1/category/", json=data, headers=token)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == "Category with this data already exists"


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Haircut"},
    ]
)
@pytest.mark.asyncio
async def test_post_category_401(ac: AsyncClient, payload):
    response = await ac.post("/v1/category/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
