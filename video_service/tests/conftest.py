import asyncio
from uuid import uuid4, UUID
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.database.db import create_models, delete_models
from app.core.config import get_settings
from app.services.token_service import TokenService
from shared.fastapi.user_data import OwnerSerializer

settings = get_settings()


def upload_file_mock(video: bytes, file_extension: str) -> str:
    return "testurl"


def delete_file_mock(file_url: str) -> str:
    pass


async def publish_mock(data: dict[Any, Any], send_method: str) -> None:
    pass


async def get_user_data_mock(user_id: UUID) -> OwnerSerializer:
    return OwnerSerializer(id=user_id, username="test")


@pytest.fixture(scope="function", autouse=True)
def mocking_functions(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.s3_service.S3Service.upload_file", upload_file_mock
    )
    monkeypatch.setattr(
        "app.services.s3_service.S3Service.delete_file", delete_file_mock
    )
    monkeypatch.setattr("app.api.video.service.publish", publish_mock)
    monkeypatch.setattr("app.api.video.service.get_user_data", get_user_data_mock)
    monkeypatch.setattr("app.api.comment.service.publish", publish_mock)
    monkeypatch.setattr("app.api.comment.service.get_user_data", get_user_data_mock)


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://localhost:5000/api/v1/")
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
