import pytest


@pytest.mark.asyncio
async def test_get_user_data(client, test_db, prefix_token) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.json()["username"] == data["username"]
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user_data(client, test_db, prefix_token) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    data = {"username": "NewTest"}
    response = await client.put("me", headers={"Authorization": f"{prefix_token} {access_token}"}, json=data)
    assert response.status_code == 200
    assert response.json()["username"] == data["username"]
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == data["username"]


@pytest.mark.asyncio
async def test_delete_user_data(client, test_db, prefix_token) -> None:
    data = {"username": "Test", "password": "Test", "repeat_password": "Test"}
    await client.post("register", json=data)
    data.pop("repeat_password")
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    data = {"username": "NewTest"}
    response = await client.delete("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 200
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 400
