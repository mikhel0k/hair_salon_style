import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_delete_specialization_204(ac: AsyncClient, token):
    """Удаление специализации без привязанных мастеров возвращает 204."""
    res = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert res.status_code == status.HTTP_201_CREATED
    specialization_id = res.json()["id"]

    response = await ac.delete(f"/v1/specialization/{specialization_id}/", headers=token)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_specialization_404(ac: AsyncClient, token):
    """Удаление несуществующей специализации возвращает 404."""
    response = await ac.delete("/v1/specialization/99999/", headers=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Specialization not found"


@pytest.mark.asyncio
async def test_delete_specialization_409_has_linked_masters(ac: AsyncClient, token):
    """Удаление специализации с привязанными мастерами возвращает 409."""
    res_spec = await ac.post("/v1/specialization/", json={"name": "Stylist"}, headers=token)
    assert res_spec.status_code == status.HTTP_201_CREATED
    specialization_id = res_spec.json()["id"]

    res_master = await ac.post(
        "/v1/master/",
        json={
            "name": "Petr",
            "phone": "+79009009091",
            "email": "petr.delete.spec@mail.ru",
            "status": "ACTIVE",
            "specialization_id": specialization_id,
        },
        headers=token,
    )
    assert res_master.status_code == status.HTTP_201_CREATED

    response = await ac.delete(f"/v1/specialization/{specialization_id}/", headers=token)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "linked masters" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_specialization_401(ac: AsyncClient, token):
    """Удаление без токена возвращает 401."""
    res = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert res.status_code == status.HTTP_201_CREATED
    specialization_id = res.json()["id"]

    response = await ac.delete(f"/v1/specialization/{specialization_id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
