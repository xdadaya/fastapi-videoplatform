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


class OverrideS3Service:
    settings = get_settings()

    @classmethod
    def upload_video(cls, video: bytes) -> str:
        return "testurl"

    @classmethod
    def delete_video(cls, file_url: str) -> None:
        pass


app.dependency_overrides[S3Service] = OverrideS3Service


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def videos_client() -> AsyncClient:
    app.dependency_overrides[S3Service] = OverrideS3Service
    client = AsyncClient(app=app, base_url='http://localhost:5000/api/v1/videos/')
    return client


@pytest.fixture(scope='session')
def comments_client() -> AsyncClient:
    client = AsyncClient(app=app, base_url='http://localhost:5000/api/v1/comments/')
    return client


@pytest.fixture
def owner_access_token() -> str:
    return f"{settings.AUTHENTICATION_HEADER_PREFIX} {TokenService.generate_token(uuid4())}"


@pytest.fixture
def viewer_access_token() -> str:
    return f"{settings.AUTHENTICATION_HEADER_PREFIX} {TokenService.generate_token(uuid4())}"


@pytest_asyncio.fixture(autouse=True, scope="function")
async def test_db():
    await create_models()
    yield
    await delete_models()
