from uuid import uuid4
from math import ceil

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.api.video.schemas import VideoCreateRequest, VideoUpdateRequest


@pytest.mark.asyncio
async def test_video_post(videos_client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_retrieve(videos_client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    response = await videos_client.get(f"/{video_id}")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_retrieve_fake_id(videos_client: AsyncClient) -> None:
    response = await videos_client.get(f"/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_video_pagination(videos_client: AsyncClient, owner_access_token: str) -> None:
    limit = 3
    videos_count = 10
    for i in range(videos_count):
        data = jsonable_encoder(
            VideoCreateRequest(title=f"Test {i}", description="Test", category="Test", video="Test")
        )
        await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    response = await videos_client.get(f"?limit={limit}")
    assert response.status_code == 200
    assert response.json()["total_pages"] == ceil(videos_count / limit)


@pytest.mark.asyncio
async def test_video_update(videos_client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(VideoUpdateRequest(title="UpdateTest", description="UpdateTest", category="UpdateTest"))
    response = await videos_client.put(f"/{video_id}", json=data, headers={"Authorization": viewer_access_token})
    assert response.status_code == 403
    response = await videos_client.get(f"/{video_id}")
    assert response.json()["title"] != data["title"]
    response = await videos_client.put(f"/{video_id}", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_delete(videos_client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    response = await videos_client.delete(f"/{video_id}", headers={"Authorization": viewer_access_token})
    assert response.status_code == 403
    response = await videos_client.get(f"/{video_id}")
    assert response.status_code == 200
    response = await videos_client.delete(f"/{video_id}", headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    response = await videos_client.get(f"/{video_id}")
    assert response.status_code == 404

