from datetime import date
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio()
async def test_check_one_record(ac: AsyncClient):
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
                  )
    response = await ac.get("/v1/record/by_phone/%2B78005553535")
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1
    response = response[0]
    assert response["id"] == 1
    assert response["date"] == str(date.today())
    assert response["time"] == "14:30:00"
    assert response["status"] == "created"
    assert response["price"] == 0
    assert response["notes"] == "Test note"
    assert response["user_id"] == 1


@pytest.mark.asyncio()
async def test_check_two_records(ac: AsyncClient):
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
                  )
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
                  )
    response = await ac.get("/v1/record/by_phone/%2B78005553535")
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 2
    assert response[0]["id"] == 1
    assert response[1]["id"] == 2


@pytest.mark.asyncio()
async def test_check_records_of_two_users(ac: AsyncClient):
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
                  )
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
                  )
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553532",
        "date": str(date.today()),
        "time": "16:30:00",
        "notes": "Test note"
    }
                  )
    response = await ac.get("/v1/record/by_phone/%2B78005553532")
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1
    assert response[0]["id"] == 3

    response = await ac.get("/v1/record/by_phone/%2B78005553535")
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 2
    assert response[0]["id"] == 1
    assert response[1]["id"] == 2