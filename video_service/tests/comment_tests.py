from math import ceil

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.api.comment.schemas import CommentCreateRequest
from app.api.video.schemas import VideoCreateRequest


@pytest.mark.asyncio
async def test_comment_post(videos_client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await videos_client.post(f"/{video_id}/comment", json=data,
                                        headers={"Authorization": owner_access_token})
    assert response.status_code == 201
    assert response.json()["text"] == data["text"]


@pytest.mark.asyncio
async def test_comment_pagination_sorting(videos_client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    limit = 2
    comments_count = 11
    sort_field = "created_at"
    for i in range(comments_count):
        data = jsonable_encoder(CommentCreateRequest(text=f"Test {i}"))
        await videos_client.post(f"/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    response = await videos_client.get(f"/{video_id}/comments?limit={limit}&sort={sort_field}")
    assert response.status_code == 200
    assert response.json()["total_pages"] == ceil(comments_count / limit)
    items_count = len(response.json()["items"])
    assert response.json()["items"][0][sort_field] < response.json()["items"][items_count-1][sort_field]

    response = await videos_client.get(f"/{video_id}/comments?limit={limit}&sort=-{sort_field}")
    assert response.status_code == 200
    items_count = len(response.json()["items"])
    assert response.json()["items"][0][sort_field] > response.json()["items"][items_count - 1][sort_field]


@pytest.mark.asyncio
async def test_comment_update(videos_client: AsyncClient, comments_client: AsyncClient, owner_access_token: str,
                              viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await videos_client.post(f"/{video_id}/comment", json=data,
                                        headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    data = jsonable_encoder(CommentCreateRequest(text="Update"))
    response = await comments_client.put(f"/{comment_id}", json=data, headers={"Authorization": viewer_access_token})
    assert response.status_code == 403

    response = await comments_client.put(f"/{comment_id}", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    assert response.json()["text"] == data["text"]


@pytest.mark.asyncio
async def test_comment_delete(videos_client: AsyncClient, comments_client: AsyncClient, owner_access_token: str,
                              viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await videos_client.post(f"/{video_id}/comment", json=data,
                                        headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    response = await comments_client.delete(f"/{comment_id}", headers={"Authorization": viewer_access_token})
    assert response.status_code == 403

    response = await comments_client.delete(f"/{comment_id}", headers={"Authorization": owner_access_token})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_like_comment(videos_client: AsyncClient, comments_client: AsyncClient, owner_access_token: str,
                            viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await videos_client.post(f"/{video_id}/comment", json=data,
                                        headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    await comments_client.post(f"{comment_id}/like", headers={"Authorization": owner_access_token})
    await comments_client.post(f"{comment_id}/like", headers={"Authorization": viewer_access_token})
    response = await videos_client.get(f"{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 2
    assert response.json()["items"][0]["rating"] == 2
    await comments_client.delete(f"{comment_id}/unlike", headers={"Authorization": viewer_access_token})
    response = await videos_client.get(f"{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 1
    assert response.json()["items"][0]["rating"] == 1


@pytest.mark.asyncio
async def test_dislike_comment(videos_client: AsyncClient, comments_client: AsyncClient, owner_access_token: str,
                               viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await videos_client.post("", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await videos_client.post(f"/{video_id}/comment", json=data,
                                        headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    await comments_client.post(f"{comment_id}/dislike", headers={"Authorization": owner_access_token})
    await comments_client.post(f"{comment_id}/dislike", headers={"Authorization": viewer_access_token})
    response = await videos_client.get(f"{video_id}/comments")
    assert response.json()["items"][0]["dislikes_amount"] == 2
    assert response.json()["items"][0]["rating"] == -2

    await comments_client.delete(f"{comment_id}/unlike", headers={"Authorization": viewer_access_token})
    response = await videos_client.get(f"{video_id}/comments")
    assert response.json()["items"][0]["dislikes_amount"] == 1
    assert response.json()["items"][0]["rating"] == -1

    await comments_client.post(f"{comment_id}/like", headers={"Authorization": owner_access_token})
    response = await videos_client.get(f"{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 1
    assert response.json()["items"][0]["dislikes_amount"] == 0
    assert response.json()["items"][0]["rating"] == 1
