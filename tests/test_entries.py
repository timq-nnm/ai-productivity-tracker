import pytest
from httpx import AsyncClient


async def create_user(client: AsyncClient) -> int:
    """Helper: создать пользователя и вернуть его id."""
    response = await client.post("/api/v1/users", json={"username": "testuser"})
    return response.json()["id"]


@pytest.mark.asyncio
async def test_create_entry(client):
    """POST /api/v1/entries — создание записи."""
    user_id = await create_user(client)
    response = await client.post(
        "/api/v1/entries",
        json={
            "user_id": user_id,
            "date": "2026-05-24",
            "sleep": 7,
            "energy": 8,
            "clarity": 7,
            "motivation": 9,
            "tasks_planned": "task1",
            "tasks_done": "task1",
            "reflection": "good day"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sleep"] == 7
    assert data["user_id"] == user_id
    assert "id" in data


@pytest.mark.asyncio
async def test_create_entry_minimal(client):
    """POST /api/v1/entries — только обязательные поля."""
    user_id = await create_user(client)
    response = await client.post(
        "/api/v1/entries",
        json={"user_id": user_id, "date": "2026-05-24"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_entries_by_user(client):
    """GET /api/v1/entries/user/{user_id}."""
    user_id = await create_user(client)
    await client.post("/api/v1/entries", json={"user_id": user_id, "date": "2026-05-20"})
    await client.post("/api/v1/entries", json={"user_id": user_id, "date": "2026-05-21"})
    response = await client.get(f"/api/v1/entries/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_entry(client):
    """PUT /api/v1/entries/{id}."""
    user_id = await create_user(client)
    create = await client.post(
        "/api/v1/entries",
        json={"user_id": user_id, "date": "2026-05-24", "sleep": 5}
    )
    entry_id = create.json()["id"]
    response = await client.put(
        f"/api/v1/entries/{entry_id}",
        json={"user_id": user_id, "date": "2026-05-24", "sleep": 9}
    )
    assert response.status_code == 200
    assert response.json()["sleep"] == 9
