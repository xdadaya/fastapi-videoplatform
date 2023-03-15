import pytest


@pytest.mark.asyncio
async def test_register_valid(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    response = await client.post("register", json=data)
    assert response.status_code == 201
    assert response.json()["username"] == data["username"]


@pytest.mark.asyncio
async def test_register_invalid_password(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "NotTest"}
    response = await client.post("register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_invalid_taken_username(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    response = await client.post("register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_valid(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    response = await client.post("login", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_invalid_password(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    data["password"] = "NotTest"
    response = await client.post("login", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_invalid_username(client, test_db) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    data["username"] = "NotTest"
    response = await client.post("login", json=data)
    assert response.status_code == 400

