import pytest
from fastapi.encoders import jsonable_encoder

from httpx import AsyncClient

from app.core.schemas.auth_schema import UserRegisterRequest, UserLoginRequest, UserSchema


@pytest.mark.asyncio
async def test_get_user_data(client: AsyncClient, prefix_token: str) -> None:
    data = jsonable_encoder(UserRegisterRequest(username="Test", password="Test", repeat_password="Test"))
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="Test", password="Test"))
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.json()["username"] == data["username"]
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user_data(client: AsyncClient, prefix_token: str) -> None:
    data = jsonable_encoder(UserRegisterRequest(username="Test", password="Test", repeat_password="Test"))
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="Test", password="Test"))
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    data = jsonable_encoder(UserSchema(username="NewTest"))
    response = await client.put("me", headers={"Authorization": f"{prefix_token} {access_token}"}, json=data)
    assert response.status_code == 200
    assert response.json()["username"] == data["username"]
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 200
    assert response.json()["username"] == data["username"]


@pytest.mark.asyncio
async def test_delete_user_data(client: AsyncClient, prefix_token: str) -> None:
    data = jsonable_encoder(UserRegisterRequest(username="Test", password="Test", repeat_password="Test"))
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="Test", password="Test"))
    response = await client.post("login", json=data)
    access_token = response.json()["access_token"]
    response = await client.delete("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 200
    response = await client.get("me", headers={"Authorization": f"{prefix_token} {access_token}"})
    assert response.status_code == 404
