import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.core.schemas.auth_schema import UserRegisterRequest, UserLoginRequest


@pytest.mark.asyncio
async def test_register_valid(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="Test")
    )
    response = await client.post("register", json=data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_register_invalid_password(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="NotTest")
    )
    response = await client.post("register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_register_invalid_taken_username(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="Test")
    )
    await client.post("register", json=data)
    response = await client.post("register", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_valid(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="Test")
    )
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="Test", password="Test"))
    response = await client.post("login", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="Test")
    )
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="Test", password="NotTest"))
    response = await client.post("login", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_invalid_username(client: AsyncClient) -> None:
    data = jsonable_encoder(
        UserRegisterRequest(username="Test", password="Test", repeat_password="Test")
    )
    await client.post("register", json=data)
    data = jsonable_encoder(UserLoginRequest(username="NotTest", password="Test"))
    response = await client.post("login", json=data)
    assert response.status_code == 400
