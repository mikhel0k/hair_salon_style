from datetime import date

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_edit_note_record(ac: AsyncClient):
    await ac.post("http://127.0.0.1:8000/v1/master/new_master", json={
        "name": "string",
        "specialization": "string",
        "phone": "string",
        "email": "string",
        "work_schedule": "string",
        "status": "string"
    })
    await ac.post("http://127.0.0.1:8000/v1/service/new_service", json={
        "name": "string",
        "price": 0,
        "duration": 0,
        "category": "string",
        "description": "string"
    })
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
        "master_id": 1,
        "service_id": 1,
        "notes": "Test note"
    }
                  )
    response = await ac.patch("/v1/record/update_note", json={
        "id": 1,
        "notes": "New note",
    })

    assert response.status_code == 200
    response = response.json()
    assert response["id"] == 1
    assert response["date"] == str(date.today())
    assert response["time"] == "14:30:00"
    assert response["status"] == "created"
    assert response["price"] == 0
    assert response["notes"] == "New note"
    assert response["service_id"] == 1
    assert response["master_id"] == 1
    assert response["user_id"] == 1
