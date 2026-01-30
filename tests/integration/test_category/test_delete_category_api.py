import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "payload",
    [
        ([{"name": "Haircut"}]),
        ([
            {"name": "Haircut"},
            {"name": "manicure"},
            {"name": "lamination    "},
            {"name": "   coloring"},
        ])
    ]
)
@pytest.mark.asyncio
async def test_get_category_200(ac: AsyncClient, payload, token):
    created_ids = []
    for p in payload:
        res = await ac.post("/v1/category/", json=p, headers=token)
        assert res.status_code == 201
        created_ids.append(res.json()["id"])

    for category_id in created_ids:
        response = await ac.delete(f"/v1/category/{category_id}/", headers=token)
        assert response.status_code == 204


@pytest.mark.parametrize(
    "payload, del_ids",
    [
        ([{"name": "Haircut"},],[2, 3]),
    ]
)
@pytest.mark.asyncio
async def test_get_category_404(ac: AsyncClient, payload, del_ids, token):
    for i in range(0, len(payload)):
        response = await ac.post("/v1/category/", json=payload[i], headers=token)
        assert response.status_code == 201

    for i in range(0, len(del_ids)):
        response = await ac.delete(f"/v1/category/{del_ids[i]}/", headers=token)
        assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        ([{"name": "Haircut"},]),
    ]
)
@pytest.mark.asyncio
async def test_get_category_401(ac: AsyncClient, payload, token):
    created_ids = []
    for p in payload:
        res = await ac.post("/v1/category/", json=p, headers=token)
        assert res.status_code == 201
        created_ids.append(res.json().get("id"))

    for category_id in created_ids:
        response = await ac.delete(f"/v1/category/{category_id}/")
        assert response.status_code == 401