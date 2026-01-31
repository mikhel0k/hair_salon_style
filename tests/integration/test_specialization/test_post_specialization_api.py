import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    "payload",
    [
        [{"name": "Barber"}],
        [
            {"name": "Barber"},
            {"name": "Manicure"},
            {"name": "  Stylist  "},
        ],
    ],
)
@pytest.mark.asyncio
async def test_post_specialization_201(ac: AsyncClient, payload, token):
    for i in range(len(payload)):
        response = await ac.post("/v1/specialization/", json=payload[i], headers=token)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == payload[i]["name"].strip().title()
        assert "id" in response.json()


@pytest.mark.parametrize(
    "payload, message",
    [
        ({"name": "123"}, "Value error, Invalid character"),
        ({"name": "ab"}, "String should have at least 3 characters"),
        ({"name": "a" * 41}, "String should have at most 40 characters"),
        ({"name": 1}, "Input should be a valid string"),
    ],
)
@pytest.mark.asyncio
async def test_post_specialization_422(ac: AsyncClient, payload, message, token):
    response = await ac.post("/v1/specialization/", json=payload, headers=token)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = response.json()["detail"]
    if isinstance(detail, list):
        assert any(message in str(d.get("msg", "")) for d in detail), f"Expected {message!r} in {detail}"
    else:
        assert message in str(detail)


@pytest.mark.asyncio
async def test_post_specialization_409(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Specialization with this data already exists"


@pytest.mark.asyncio
async def test_post_specialization_401(ac: AsyncClient):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"
