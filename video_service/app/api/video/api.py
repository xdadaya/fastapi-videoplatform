from uuid import UUID

from fastapi import APIRouter, Depends
from app.api.video.schemas import (
    VideoCreateFormRequest,
    VideoSerializer,
    VideoUpdateRequest,
    VideoListResponse,
)
from app.api.comment.schemas import (
    CommentCreateRequest,
    CommentSerializer,
    CommentListResponse,
)
from app.api.video.service import VideoService
from app.api.comment.service import CommentService
from shared.fastapi.middleware.middleware import verify_token, get_user_id
from app.core.fastapi.middleware.middleware import is_video_owner


api = APIRouter(
    prefix="/videos",
)


@api.get("/", response_model=VideoListResponse)
async def get_all_videos(page: int = 1, limit: int = 10) -> VideoListResponse:
    return await VideoService.pagination_list(page=page, limit=limit)


@api.get("/{video_id}", response_model=VideoSerializer)
async def get_video_by_id(video_id: UUID) -> VideoSerializer:
    return await VideoService.retrieve(video_id)


@api.post("/", response_model=VideoSerializer, status_code=201)
async def post_video(
    video_data: VideoCreateFormRequest = Depends(VideoCreateFormRequest.as_form),
    user_id: UUID = Depends(verify_token),
) -> VideoSerializer:
    return await VideoService.create(video_data, user_id)


@api.put(
    "/{video_id}",
    response_model=VideoSerializer,
    dependencies=[Depends(is_video_owner)],
)
async def update_video(video_id: UUID, video: VideoUpdateRequest) -> VideoSerializer:
    return await VideoService.update(video_id, video)


@api.delete("/{video_id}", dependencies=[Depends(is_video_owner)])
async def delete_video(video_id: UUID) -> None:
    await VideoService.delete(video_id)


@api.post("/{video_id}/comment", response_model=CommentSerializer, status_code=201)
async def create_comment(
    video_id: UUID, comment: CommentCreateRequest, user_id: UUID = Depends(verify_token)
) -> CommentSerializer:
    return await CommentService.create(video_id, user_id, comment)


@api.get("/{video_id}/comments", response_model=CommentListResponse)
async def get_comments_by_video_id(
    video_id: UUID,
    page: int = 1,
    limit: int = 10,
    sort: str = None,
    user_id: UUID = Depends(get_user_id),
) -> CommentListResponse:
    return await CommentService.list_by_video_id(video_id, page, limit, sort, user_id)
