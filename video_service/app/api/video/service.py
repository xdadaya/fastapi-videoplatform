from math import ceil
from typing import List
from uuid import UUID, uuid4
import cv2
import os

from app.api.video.schemas import (
    VideoSerializer,
    VideoCreateSchema,
    VideoCreateFormRequest,
    VideoUpdateRequest,
    VideoUpdateSchema,
    VideoListResponse,
)
from app.core.crud.category_crud import CategoryCRUD
from app.core.crud.video_crud import VideoCRUD
from app.core.crud.comment_crud import CommentCRUD
from app.core.crud.comment_reaction_crud import CommentReactionCRUD
from app.core.schemas.update_statistics_schema import UpdateSchema
from app.services.s3_service import S3Service
from shared.fastapi.exceptions.exc import NotVideoException, FrameUploadException
from app.producer import publish
from shared.fastapi.user_data import get_user_data


class VideoService:
    @staticmethod
    async def list() -> List[VideoSerializer]:
        return await VideoCRUD.list_items()

    @staticmethod
    async def pagination_list(page: int, limit: int) -> VideoListResponse:
        count = await VideoCRUD.count_query()
        total_pages = ceil(count / limit)
        videos = await VideoCRUD.list_items_with_pagination(page=page, limit=limit)
        result = []
        for video in videos:
            owner_data = await get_user_data(video.owner_id)
            result.append(VideoSerializer(owner=owner_data, **vars(video)))
        return VideoListResponse(
            page_number=page, page_size=limit, total_pages=total_pages, items=result
        )

    @staticmethod
    async def retrieve(video_id: UUID) -> VideoSerializer:
        video = await VideoCRUD.retrieve(id=video_id)
        owner_data = await get_user_data(video.owner_id)
        return VideoSerializer(owner=owner_data, **vars(video))

    @staticmethod
    async def create(
        video_data: VideoCreateFormRequest, user_id: UUID
    ) -> VideoSerializer:
        if not video_data.video.filename.endswith(".mp4"):
            raise NotVideoException()

        video_id = uuid4()
        video_bytes = await video_data.video.read()
        with open(f"{video_id}.mp4", "wb") as out_file:
            out_file.write(video_bytes)

        vidcap = cv2.VideoCapture(f"{video_id}.mp4")
        frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        video_length = round(frame_count / fps)
        success, image = vidcap.read()
        if not success:
            raise FrameUploadException
        is_success, im_buf_arr = cv2.imencode(".jpg", image)
        if not is_success:
            raise FrameUploadException
        byte_im = im_buf_arr.tobytes()
        first_frame_url = S3Service.upload_file(byte_im, ".jpg")

        os.remove(f"{video_id}.mp4")

        video_url = S3Service.upload_file(video_bytes, ".mp4")
        category = await CategoryCRUD.get_or_create(name=video_data.category)
        video = VideoCreateSchema(
            id=video_id,
            title=video_data.title,
            description=video_data.description,
            video_url=video_url,
            first_frame_url=first_frame_url,
            video_length=video_length,
            owner_id=user_id,
            category_id=category.id,
        )
        await VideoCRUD.create(video)
        data = UpdateSchema(user_id=str(user_id), videos_amount=1)
        await publish(send_method="update_stats", data=data.dict())
        created_video = await VideoCRUD.retrieve(id=video_id)
        owner_data = await get_user_data(video.owner_id)
        return VideoSerializer(owner=owner_data, **vars(created_video))

    @staticmethod
    async def update(video_id: UUID, video: VideoUpdateRequest) -> VideoSerializer:
        category = await CategoryCRUD.get_or_create(name=video.category)
        video = VideoUpdateSchema(
            title=video.title, description=video.description, category_id=category.id
        )
        await VideoCRUD.update(id=video_id, input_data=video)
        created_video = await VideoCRUD.retrieve(id=video_id)
        owner_data = await get_user_data(created_video.owner_id)
        return VideoSerializer(owner=owner_data, **vars(created_video))

    @staticmethod
    async def delete(video_id: UUID) -> None:
        video = await VideoCRUD.retrieve(id=video_id)
        S3Service.delete_file(video.video_url)
        S3Service.delete_file(video.first_frame_url)
        user_id = video.owner_id
        comments_amount_by_video_id = await CommentCRUD.count_query(video_id=video_id)
        comments_amount, total_text_length, total_rating = 0, 0, 0
        for _ in range(comments_amount_by_video_id):
            comment = await CommentCRUD.retrieve(video_id=video_id)
            comments_amount += 1
            comment_text = comment.text
            comment_rating = comment.rating
            comment_id = comment.id
            total_text_length += len(comment_text)
            total_rating += comment_rating
            await CommentReactionCRUD.delete(comment_id=comment_id)
        await VideoCRUD.delete(id=video_id)
        await CommentCRUD.delete(video_id=video_id)
        data = UpdateSchema(
            user_id=str(user_id),
            videos_amount=-1,
            comments_amount=-comments_amount,
            total_text_length=-total_text_length,
            total_rating=-total_rating,
        )
        await publish(send_method="update_stats", data=data.dict())
