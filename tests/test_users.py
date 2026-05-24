import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    """POST /api/v1/users — создание пользователя."""
    response = await client.post(
        "/api/v1/users",
        json={"username": "alice"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_duplicate_user(client):
    """POST /api/v1/users — дубликат возвращает 409."""
    await client.post("/api/v1/users", json={"username": "bob"})
    response = await client.post("/api/v1/users", json={"username": "bob"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_all_users(client):
    """GET /api/v1/users — пустой список."""
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(client):
    """GET /api/v1/users/{id} — получение по id."""
    create = await client.post("/api/v1/users", json={"username": "carol"})
    user_id = create.json()["id"]
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "carol"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    """GET /api/v1/users/{id} — несуществующий id."""
    response = await client.get("/api/v1/users/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_username(client):
    """GET /api/v1/users/by-username/{username}."""
    await client.post("/api/v1/users", json={"username": "dave"})
    response = await client.get("/api/v1/users/by-username/dave")
    assert response.status_code == 200
    assert response.json()["username"] == "dave"


@pytest.mark.asyncio
async def test_delete_user(client):
    """DELETE /api/v1/users/{id}."""
    create = await client.post("/api/v1/users", json={"username": "eve"})
    user_id = create.json()["id"]
    response = await client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
