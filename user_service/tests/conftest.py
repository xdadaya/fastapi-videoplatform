import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from typing import Any

from app.main import app
from app.database.db import create_models, delete_models
from app.core.config import get_settings


async def publish_mock(data: dict[Any, Any], send_method: str) -> None:
    pass


@pytest.fixture(scope="function", autouse=True)
def mocking_functions(monkeypatch) -> None:
    monkeypatch.setattr("app.api.auth_service.publish", publish_mock)
    monkeypatch.setattr("app.api.user_service.publish", publish_mock)


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://localhost:5000/api/v1/users/")
    return client


@pytest.fixture
def prefix_token() -> str:
    settings = get_settings()
    return settings.AUTHENTICATION_HEADER_PREFIX


@pytest_asyncio.fixture(autouse=True, scope="function")
async def test_db():
    await create_models()
    yield
    await delete_models()
