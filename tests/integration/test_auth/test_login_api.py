import pytest
from httpx import AsyncClient
from starlette import status
from app.core.security import decode_token
from tests.integration.conftest import CORRECT_LOGIN, CORRECT_PASSWORD


@pytest.mark.asyncio
async def test_login_200(ac: AsyncClient, redis_client):
    """Логин возвращает jti; код берём из Redis; login_confirm возвращает success и выставляет cookies."""
    payload = {"username": CORRECT_LOGIN, "password": CORRECT_PASSWORD}

    response = await ac.post("/v1/auth/login/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    jti = response.json()
    assert isinstance(jti, str), "Ожидается jti (строка)"
    assert len(jti) == 36, "jti должен быть UUID"

    code = redis_client.get(f"login_confirm_jti:{jti}")
    assert code, "Код должен быть в Redis"

    resp_confirm = await ac.post("/v1/auth/login/confirm/", json={"code": code, "jti": jti})
    assert resp_confirm.status_code == status.HTTP_200_OK
    assert resp_confirm.json() == {"status": "success"}

    token = resp_confirm.cookies.get("access_token")
    assert token is not None, "Access token cookie missing"

    decoded_token = decode_token(token)
    assert decoded_token["sub"] == "1"
    assert decoded_token["master_id"] is None
    assert decoded_token["is_master"] is False
    assert decoded_token["is_admin"] is True
    assert decoded_token["is_active"] is True


@pytest.mark.parametrize(
    "payload",
    [
        {"username": "Wrong_admin", "password": "qwerty123"},
        {"username": CORRECT_LOGIN, "password": "qwerty123"}
    ]
)
@pytest.mark.asyncio
async def test_login_wrong_401(payload, ac: AsyncClient):
    response = await ac.post("/v1/auth/login/", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail" : "Worker login or password is incorrect"}


@pytest.mark.parametrize(
    "payload, message",
    [
        ({"username": "a" * 2, "password": "qwerty123"}, "String should have at least 3 characters"),
        ({"username": "a" * 31, "password": "qwerty123"}, "String should have at most 30 characters"),
        ({"username": 1, "password": "qwerty123"}, "Input should be a valid string"),
        ({"username": 1.5, "password": "qwerty123"}, "Input should be a valid string"),
        ({"username": True, "password": "qwerty123"}, "Input should be a valid string"),
        ({"username": False, "password": "qwerty123"}, "Input should be a valid string"),
        ({"username": None, "password": "qwerty123"}, "Input should be a valid string"),
    ]
)
@pytest.mark.asyncio
async def test_login_wrong_422(payload, message, ac: AsyncClient):
    response = await ac.post("/v1/auth/login/", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()["detail"][0]["msg"] == message
