import pytest
from httpx import AsyncClient


async def create_user_and_entries(client):
    """Helper: создать пользователя с 3 записями за последние 3 дня."""
    from datetime import date, timedelta
    user_resp = await client.post("/api/v1/users", json={"username": "analyticsuser"})
    user_id = user_resp.json()["id"]
    today = date.today()
    for i in range(3):
        d = (today - timedelta(days=i)).isoformat()
        await client.post(
            "/api/v1/entries",
            json={
                "user_id": user_id,
                "date": d,
                "sleep": 7,
                "energy": 8,
                "clarity": 7,
                "motivation": 9,
                "reflection": f"reflection {i}"
            }
        )
    return user_id


@pytest.mark.asyncio
async def test_burnout_endpoint(client):
    """GET /api/v1/analytics/burnout/{user_id}."""
    user_id = await create_user_and_entries(client)
    response = await client.get(f"/api/v1/analytics/burnout/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "level" in data
    assert "metrics" in data


@pytest.mark.asyncio
async def test_streak_endpoint(client):
    """GET /api/v1/analytics/streak/{user_id}."""
    user_id = await create_user_and_entries(client)
    response = await client.get(f"/api/v1/analytics/streak/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "current_streak" in data
    assert data["current_streak"] >= 1


@pytest.mark.asyncio
async def test_trends_endpoint(client):
    """GET /api/v1/analytics/trends/{user_id}."""
    user_id = await create_user_and_entries(client)
    response = await client.get(f"/api/v1/analytics/trends/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert "trends" in data or "error" in data
