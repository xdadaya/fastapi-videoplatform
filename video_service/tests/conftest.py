import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.database.db import create_models, delete_models
from app.core.config import get_settings
from app.services.token_service import TokenService
from app.services.s3_service import S3Service

settings = get_settings()


def upload_video_mock(video: bytes) -> str:
    return "testurl"


@pytest.fixture(scope="function", autouse=True)
def change_upload_video(monkeypatch) -> None:
    monkeypatch.setattr(S3Service, "upload_video", upload_video_mock)


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def client() -> AsyncClient:
    client = AsyncClient(app=app, base_url='http://localhost:5000/api/v1/')
    return client


@pytest.fixture
def owner_access_token() -> str:
    access_token = TokenService.generate_token(uuid4())
    return f"{settings.AUTHENTICATION_HEADER_PREFIX} {access_token}"


@pytest.fixture
def viewer_access_token() -> str:
    access_token = TokenService.generate_token(uuid4())
    return f"{settings.AUTHENTICATION_HEADER_PREFIX} {access_token}"


@pytest_asyncio.fixture(autouse=True, scope="function")
async def test_db():
    await create_models()
    yield
    await delete_models()
