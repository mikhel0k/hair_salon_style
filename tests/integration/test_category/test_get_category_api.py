import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    "payload, ans_len",
    [
        ([{"name": "Haircut"},],1),
        ([
            {"name": "Haircut"},
            {"name": "manicure"},
            {"name": "lamination    "},
            {"name": "   coloring"},
        ],4),
        ([
            {"name": "Haircut"},
            {"name": "Haircut"},
        ],1),
        ([], 0)
    ]
)
@pytest.mark.asyncio
async def test_get_category_200(ac: AsyncClient, payload, ans_len, token):
    for i in range(0, len(payload)):
        response = await ac.post("/v1/category/", json=payload[i], headers=token)

    response = await ac.get("/v1/category/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == ans_len

