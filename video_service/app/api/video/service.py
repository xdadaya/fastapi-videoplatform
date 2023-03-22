from math import ceil
from typing import List
from uuid import UUID, uuid4

from app.api.video.schemas import VideoSerializer, VideoCreateSchema, VideoCreateRequest, VideoUpdateRequest, \
    VideoUpdateSchema, VideoListResponse
from app.core.crud.category_crud import CategoryCRUD
from app.core.crud.video_crud import VideoCRUD
from app.services.s3_service import S3Service


class VideoService:
    @staticmethod
    async def list() -> List[VideoSerializer]:
        return await VideoCRUD.list_items()

    @staticmethod
    async def pagination_list(page: int, limit: int) -> VideoListResponse:
        count = await VideoCRUD.count_query()
        total_pages = ceil(count / limit)
        result = await VideoCRUD.list_items_with_pagination(page=page, limit=limit)
        return VideoListResponse(page_number=page, page_size=limit, total_pages=total_pages, items=result)

    @staticmethod
    async def retrieve(video_id: UUID) -> VideoSerializer:
        return await VideoCRUD.retrieve(id=video_id)

    @staticmethod
    async def create(video_data: VideoCreateRequest, user_id: UUID) -> VideoSerializer:
        video_url = S3Service.upload_video(video_data.video)
        video_id = uuid4()
        category = await CategoryCRUD.get_or_create(name=video_data.category)
        video = VideoCreateSchema(id=video_id, title=video_data.title, description=video_data.description,
                                  video_url=video_url, owner_id=user_id, category_id=category.id)
        await VideoCRUD.create(video)
        return await VideoCRUD.retrieve(id=video_id)

    @staticmethod
    async def update(video_id: UUID, video: VideoUpdateRequest) -> VideoSerializer:
        category = await CategoryCRUD.get_or_create(name=video.category)
        video = VideoUpdateSchema(title=video.title, description=video.description, category_id=category.id)
        await VideoCRUD.update(id=video_id, input_data=video)
        return await VideoCRUD.retrieve(id=video_id)

    @staticmethod
    async def delete(video_id: UUID) -> None:
        video = await VideoCRUD.retrieve(id=video_id)
        S3Service.delete_video(video.video_url)
        await VideoCRUD.delete(id=video_id)
