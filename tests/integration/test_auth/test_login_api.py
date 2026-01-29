import pytest
from httpx import AsyncClient
from starlette import status
from app.core.security import decode_token


@pytest.mark.asyncio
async def test_login_right(ac: AsyncClient):
    payload = {"username": "I_am_admin", "password": "Zxc-q123"}

    response = await ac.post("/v1/auth/login", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status" : "success"}

    token = decode_token(response.cookies.get("access_token"))
    assert token["sub"] == "1"
    assert token["master_id"] is None
    assert token["is_master"] == False
    assert token["is_admin"] == True
    assert token["is_active"] == True


@pytest.mark.asyncio
async def test_login_wrong_username(ac: AsyncClient):
    payload = {"username": "Wrong_admin", "password": "qwerty123"}

    response = await ac.post("/v1/auth/login", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail" : "Worker login or password is incorrect"}


@pytest.mark.asyncio
async def test_login_wrong_password(ac: AsyncClient):
    payload = {"username": "I_am_admin", "password": "qwerty123"}

    response = await ac.post("/v1/auth/login", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail" : "Worker login or password is incorrect"}
