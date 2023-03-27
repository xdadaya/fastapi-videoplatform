from uuid import UUID, uuid4
from math import ceil

from app.api.comment.schemas import CommentCreateRequest, CommentCreateSchema, CommentSerializer, ReactionTypeSchema,\
    ReactionCreateSchema, CommentListResponse
from app.core.crud.comment_crud import CommentCRUD
from app.core.crud.video_crud import VideoCRUD
from app.core.crud.comment_reaction_crud import CommentReactionCRUD
from app.database.models.enums.reaction_type_enum import ReactionType
from app.core.fastapi.exceptions import NotFoundException
from app.producer import publish


class CommentService:
    @staticmethod
    async def create(video_id: UUID, user_id: UUID, comment: CommentCreateRequest) -> CommentSerializer:
        comment_id = uuid4()
        comment = CommentCreateSchema(text=comment.text, id=comment_id, owner_id=user_id, video_id=video_id)
        await CommentCRUD.create(comment)
        comment = await CommentCRUD.retrieve(id=comment_id)
        video = await VideoCRUD.retrieve(id=video_id)
        data = {"user_id": str(video.owner_id), "comments_amount": 1, "total_text_length": len(comment.text)}
        await publish(send_method="update_stats", data=data)
        return comment

    @staticmethod
    async def list_by_video_id(video_id: UUID, page: int, limit: int, sort: str) -> CommentListResponse:
        count = await CommentCRUD.count_query(video_id=video_id)
        total_pages = ceil(count / limit)
        result = await CommentCRUD.list_items_with_pagination(page=page, limit=limit, sort=sort, video_id=video_id)
        return CommentListResponse(page_number=page, page_size=limit, total_pages=total_pages, items=result)

    @staticmethod
    async def update(comment_id: UUID, comment_update: CommentCreateRequest) -> CommentSerializer:
        comment = await CommentCRUD.retrieve(id=comment_id)
        old_text_length = len(comment.text)
        await CommentCRUD.update(id=comment_id, input_data=comment_update)
        comment = await CommentCRUD.retrieve(id=comment_id)
        new_text_length = len(comment.text)
        video = await VideoCRUD.retrieve(id=comment.video_id)
        data = {"user_id": str(video.owner_id), "total_text_length": new_text_length - old_text_length}
        await publish(send_method="update_stats", data=data)
        return comment

    @staticmethod
    async def delete(comment_id: UUID) -> None:
        comment = await CommentCRUD.retrieve(id=comment_id)
        video = await VideoCRUD.retrieve(id=comment.video_id)
        owner_id = video.owner_id
        data = {'user_id': str(owner_id), "comments_amount": -1,
                "total_text_length": -len(comment.text), "total_rating": -comment.rating}
        await CommentCRUD.delete(id=comment_id)
        await CommentReactionCRUD.delete(comment_id=comment_id)
        await publish(send_method="update_stats", data=data)

    @staticmethod
    async def like(comment_id: UUID, user_id: UUID) -> None:
        comment = await CommentCRUD.retrieve(id=comment_id)
        old_rating = comment.rating
        video = await VideoCRUD.retrieve(id=comment.video_id)
        owner_id = video.owner_id
        try:
            comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
            data = ReactionTypeSchema(reaction_type=ReactionType.LIKE)
            await CommentReactionCRUD.update(id=comment_reaction.id, input_data=data)
        except NotFoundException:
            data = ReactionCreateSchema(comment_id=comment_id, owner_id=user_id, reaction_type=ReactionType.LIKE)
            await CommentReactionCRUD.create(data)
        comment = await CommentCRUD.retrieve(id=comment_id)
        new_rating = comment.rating
        data = {"user_id": str(owner_id), "total_rating": new_rating - old_rating}
        await publish(send_method="update_stats", data=data)

    @staticmethod
    async def dislike(comment_id: UUID, user_id: UUID) -> None:
        comment = await CommentCRUD.retrieve(id=comment_id)
        old_rating = comment.rating
        video = await VideoCRUD.retrieve(id=comment.video_id)
        owner_id = video.owner_id
        try:
            comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
            data = ReactionTypeSchema(reaction_type=ReactionType.DISLIKE)
            await CommentReactionCRUD.update(id=comment_reaction.id, input_data=data)
        except NotFoundException:
            data = ReactionCreateSchema(comment_id=comment_id, owner_id=user_id, reaction_type=ReactionType.DISLIKE)
            await CommentReactionCRUD.create(data)
        comment = await CommentCRUD.retrieve(id=comment_id)
        new_rating = comment.rating
        data = {"user_id": str(owner_id), "total_rating": new_rating - old_rating}
        await publish(send_method="update_stats", data=data)

    @staticmethod
    async def unlike(comment_id: UUID, user_id: UUID) -> None:
        comment = await CommentCRUD.retrieve(id=comment_id)
        old_rating = comment.rating
        video = await VideoCRUD.retrieve(id=comment.video_id)
        owner_id = video.owner_id
        comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
        await CommentReactionCRUD.delete(id=comment_reaction.id)
        comment = await CommentCRUD.retrieve(id=comment_id)
        new_rating = comment.rating
        data = {"user_id": str(owner_id), "total_rating": new_rating - old_rating}
        await publish(send_method="update_stats", data=data)
