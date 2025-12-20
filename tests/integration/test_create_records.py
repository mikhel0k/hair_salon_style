from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_record_today(ac: AsyncClient):
    payload = {
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    assert response.status_code == 200
    response = response.json()

    assert response["id"] == 1
    assert response["date"] == payload["date"]
    assert response["time"] == payload["time"]
    assert response["status"] == "created"
    assert response["price"] == 0
    assert response["notes"] == payload["notes"]
    assert response["user_id"] == 1


@pytest.mark.asyncio
async def test_create_record_yesterday(ac: AsyncClient):
    payload = {
        "phone_number": "+78005553535",
        "date": str(date.today() - timedelta(days=1)),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    assert response.status_code == 422
    response = response.json()["detail"]
    assert len(response) == 1
    response = response[0]

    assert response["type"] == "value_error"
    assert response["msg"] == "Value error, Date must be in the future"


@pytest.mark.asyncio
async def test_create_record_without_notes(ac: AsyncClient):
    payload = {
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    assert response.status_code == 200
    response = response.json()

    assert response["id"] == 1
    assert response["date"] == payload["date"]
    assert response["time"] == payload["time"]
    assert response["status"] == "created"
    assert response["price"] == 0
    assert response["notes"] is None
    assert response["user_id"] == 1


@pytest.mark.asyncio
async def test_create_record_with_wrong_phone(ac: AsyncClient):
    payload = {
        "phone_number": "+7800555353",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    assert response.status_code == 422
    response = response.json()["detail"]
    assert len(response) == 1
    response = response[0]

    assert response["type"] == "value_error"
    assert response["msg"] == "Value error, Invalid phone format"


@pytest.mark.asyncio
async def test_create_record_with_three_records(ac: AsyncClient):
    payload = {
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)
    assert response.status_code == 200

    payload = {
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)
    assert response.status_code == 200

    payload = {
        "phone_number": "+78005553533",
        "date": str(date.today()),
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    assert response.status_code == 200
    response = response.json()

    assert response["id"] == 3
    assert response["date"] == payload["date"]
    assert response["time"] == payload["time"]
    assert response["status"] == "created"
    assert response["price"] == 0
    assert response["notes"] == payload["notes"]
    assert response["user_id"] == 2
