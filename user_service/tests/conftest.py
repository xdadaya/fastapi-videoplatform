import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.database.db import create_models, delete_models
from app.core.config import get_settings


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def client():
    client = AsyncClient(app=app, base_url='http://127.0.0.1:5000/api/v1/users/')
    return client


@pytest.fixture
def prefix_token():
    settings = get_settings()
    return settings.AUTHENTICATION_HEADER_PREFIX



@pytest_asyncio.fixture()
async def test_db():
    await create_models()
    yield
    await delete_models()
