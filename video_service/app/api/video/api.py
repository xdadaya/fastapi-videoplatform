from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, Query
from app.api.video.schemas import VideoCreateRequest, VideoSerializer, VideoUpdateRequest
from app.api.comment.schemas import CommentCreateRequest, CommentSerializer, CommentListResponse
from app.api.video.service import VideoService
from app.api.comment.service import CommentService
from app.services.middleware import verify_token, is_video_owner


api = APIRouter(prefix="/videos", )


@api.get("/", response_model=List[VideoSerializer])
async def get_all_videos() -> List[VideoSerializer]:
    return await VideoService.list()


@api.get("/{video_id}", response_model=VideoSerializer)
async def get_video_by_id(video_id: UUID) -> VideoSerializer:
    return await VideoService.retrieve(video_id)


@api.post("/", response_model=VideoSerializer)
async def post_video(video_data: VideoCreateRequest, user_id: UUID = Depends(verify_token),) -> VideoSerializer:
    return await VideoService.create(video_data, user_id)


@api.put("/{video_id}", response_model=VideoSerializer, dependencies=[Depends(is_video_owner)])
async def update_video(video_id: UUID, video: VideoUpdateRequest) -> VideoSerializer:
    return await VideoService.update(video_id, video)


@api.delete("/{video_id}", dependencies=[Depends(is_video_owner)])
async def delete_video(video_id: UUID) -> None:
    await VideoService.delete(video_id)


@api.post("/{video_id}/comment", response_model=CommentSerializer)
async def create_comment(video_id: UUID, comment: CommentCreateRequest, user_id: UUID = Depends(verify_token)) -> CommentSerializer:
    return await CommentService.create(video_id, user_id, comment)


@api.get("/{video_id}/comments", response_model=CommentListResponse)
async def get_comments_by_video_id(video_id: UUID, page: int = 1, limit: int = 10,
                                   sort: str = Query(None, alias="sort")) -> CommentListResponse:
    return await CommentService.list_by_video_id(video_id, page, limit, sort)
