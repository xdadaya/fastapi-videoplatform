from uuid import uuid4
from math import ceil

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.api.video.schemas import VideoCreateRequest, VideoUpdateRequest


@pytest.mark.asyncio
async def test_video_post(client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_retrieve(client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    response = await client.get(f"videos/{video_id}")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_retrieve_fake_id(client: AsyncClient) -> None:
    response = await client.get(f"videos/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_video_pagination(client: AsyncClient, owner_access_token: str) -> None:
    limit = 3
    videos_count = 10
    for i in range(videos_count):
        data = jsonable_encoder(
            VideoCreateRequest(title=f"Test {i}", description="Test", category="Test", video="Test")
        )
        await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    response = await client.get(f"videos/?limit={limit}")
    assert response.status_code == 200
    assert response.json()["total_pages"] == ceil(videos_count / limit)


@pytest.mark.asyncio
async def test_video_update(client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(VideoUpdateRequest(title="UpdateTest", description="UpdateTest", category="UpdateTest"))
    response = await client.put(f"videos/{video_id}", json=data, headers={"Authorization": viewer_access_token})
    assert response.status_code == 403
    response = await client.get(f"videos/{video_id}")
    assert response.json()["title"] != data["title"]
    response = await client.put(f"videos/{video_id}", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]


@pytest.mark.asyncio
async def test_video_delete(client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    response = await client.delete(f"videos/{video_id}", headers={"Authorization": viewer_access_token})
    assert response.status_code == 403
    response = await client.get(f"videos/{video_id}")
    assert response.status_code == 200
    response = await client.delete(f"videos/{video_id}", headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    response = await client.get(f"videos/{video_id}")
    assert response.status_code == 404

