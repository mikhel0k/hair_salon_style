from datetime import date

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio()
async def test_edit_note_record(ac: AsyncClient):
    await ac.post("/v1/record/create_record", json={
        "phone_number": "+78005553535",
        "date": str(date.today()),
        "time": "14:30:00",
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
    assert response["user_id"] == 1
