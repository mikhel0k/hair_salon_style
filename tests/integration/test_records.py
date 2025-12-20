import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_record(ac: AsyncClient):
    payload = {
        "phone_number": "+79161234567",
        "date": "2025-12-30",
        "time": "14:30:00",
        "notes": "Test note"
    }
    response = await ac.post("/v1/record/create_record", json=payload)

    # Если 500, выведи детали (в консоль при запуске pytest -s)
    if response.status_code == 500:
        print(f"\nSERVER ERROR: {response.text}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_records_by_phone(ac: AsyncClient):
    phone = "+79161234567"
    # Сначала создаем запись, потом ищем
    await ac.post("/v1/record/create_record", json={
        "phone_number": phone, "date": "2025-12-30", "time": "10:00:00"
    })

    response = await ac.get(f"/v1/record/by_phone/{phone}")
    assert response.status_code == 200
    assert len(response.json()) > 0