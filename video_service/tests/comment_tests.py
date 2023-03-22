from math import ceil

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.api.comment.schemas import CommentCreateRequest
from app.api.video.schemas import VideoCreateRequest


@pytest.mark.asyncio
async def test_comment_post(client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 201
    assert response.json()["text"] == data["text"]


@pytest.mark.asyncio
async def test_comment_pagination_sorting(client: AsyncClient, owner_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    limit = 2
    comments_count = 11
    sort_field = "created_at"
    for i in range(comments_count):
        data = jsonable_encoder(CommentCreateRequest(text=f"Test {i}"))
        await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    response = await client.get(f"videos/{video_id}/comments?limit={limit}&sort={sort_field}")
    assert response.status_code == 200
    assert response.json()["total_pages"] == ceil(comments_count / limit)
    items_count = len(response.json()["items"])
    assert response.json()["items"][0][sort_field] < response.json()["items"][items_count-1][sort_field]

    response = await client.get(f"videos/{video_id}/comments?limit={limit}&sort=-{sort_field}")
    assert response.status_code == 200
    items_count = len(response.json()["items"])
    assert response.json()["items"][0][sort_field] > response.json()["items"][items_count - 1][sort_field]


@pytest.mark.asyncio
async def test_comment_update(client: AsyncClient, owner_access_token: str,
                              viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    data = jsonable_encoder(CommentCreateRequest(text="Update"))
    response = await client.put(f"comments/{comment_id}", json=data, headers={"Authorization": viewer_access_token})
    assert response.status_code == 403

    response = await client.put(f"comments/{comment_id}", json=data, headers={"Authorization": owner_access_token})
    assert response.status_code == 200
    assert response.json()["text"] == data["text"]


@pytest.mark.asyncio
async def test_comment_delete(client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    response = await client.delete(f"comments/{comment_id}", headers={"Authorization": viewer_access_token})
    assert response.status_code == 403

    response = await client.delete(f"comments/{comment_id}", headers={"Authorization": owner_access_token})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_like_comment(client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    await client.post(f"comments/{comment_id}/like", headers={"Authorization": owner_access_token})
    await client.post(f"comments/{comment_id}/like", headers={"Authorization": viewer_access_token})
    response = await client.get(f"videos/{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 2
    assert response.json()["items"][0]["rating"] == 2
    await client.delete(f"comments/{comment_id}/unlike", headers={"Authorization": viewer_access_token})
    response = await client.get(f"videos/{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 1
    assert response.json()["items"][0]["rating"] == 1


@pytest.mark.asyncio
async def test_dislike_comment(client: AsyncClient, owner_access_token: str, viewer_access_token: str) -> None:
    data = jsonable_encoder(VideoCreateRequest(title="Test", description="Test", category="Test", video="Test"))
    response = await client.post("videos/", json=data, headers={"Authorization": owner_access_token})
    video_id = response.json()["id"]
    data = jsonable_encoder(CommentCreateRequest(text="Test"))
    response = await client.post(f"videos/{video_id}/comment", json=data, headers={"Authorization": owner_access_token})
    comment_id = response.json()["id"]

    await client.post(f"comments/{comment_id}/dislike", headers={"Authorization": owner_access_token})
    await client.post(f"comments/{comment_id}/dislike", headers={"Authorization": viewer_access_token})
    response = await client.get(f"videos/{video_id}/comments")
    assert response.json()["items"][0]["dislikes_amount"] == 2
    assert response.json()["items"][0]["rating"] == -2

    await client.delete(f"comments/{comment_id}/unlike", headers={"Authorization": viewer_access_token})
    response = await client.get(f"videos/{video_id}/comments")
    assert response.json()["items"][0]["dislikes_amount"] == 1
    assert response.json()["items"][0]["rating"] == -1

    await client.post(f"comments/{comment_id}/like", headers={"Authorization": owner_access_token})
    response = await client.get(f"videos/{video_id}/comments")
    assert response.json()["items"][0]["likes_amount"] == 1
    assert response.json()["items"][0]["dislikes_amount"] == 0
    assert response.json()["items"][0]["rating"] == 1
