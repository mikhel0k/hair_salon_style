import pytest
from httpx import AsyncClient
from starlette import status


@pytest.fixture
async def specialization_id(ac: AsyncClient, token):
    response = await ac.post("/v1/specialization/", json={"name": "Barber"}, headers=token)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


def master_payload(specialization_id, name="Petr", status="ACTIVE"):
    return {
        "specialization_id": specialization_id,
        "name": name,
        "status": status,
    }
