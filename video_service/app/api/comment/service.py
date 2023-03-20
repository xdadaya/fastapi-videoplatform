from uuid import UUID, uuid4
from math import ceil

from app.api.comment.schemas import CommentCreateRequest, CommentCreateSchema, CommentSerializer, ReactionTypeSchema,\
    ReactionCreateSchema, CommentListResponse
from app.core.crud.comment_crud import CommentCRUD
from app.core.crud.comment_reaction_crud import CommentReactionCRUD
from app.database.models.enums.reaction_type_enum import ReactionType
from app.core.fastapi.exceptions import NotFoundException


class CommentService:
    @staticmethod
    async def create(video_id: UUID, user_id: UUID, comment: CommentCreateRequest) -> CommentSerializer:
        comment_id = uuid4()
        comment = CommentCreateSchema(text=comment.text, id=comment_id, owner_id=user_id, video_id=video_id)
        await CommentCRUD.create(comment)
        return await CommentCRUD.retrieve(id=comment_id)

    @staticmethod
    async def list_by_video_id(video_id: UUID, page: int, limit: int, sort: str) -> CommentListResponse:
        count = await CommentCRUD.count_query(video_id=video_id)
        total_pages = ceil(count / limit)
        result = await CommentCRUD.list_items_with_pagination(page=page, limit=limit, sort=sort, video_id=video_id)
        return CommentListResponse(page_number=page, page_size=limit, total_pages=total_pages, items=result)

    @staticmethod
    async def update(comment_id: UUID, comment: CommentCreateRequest) -> CommentSerializer:
        await CommentCRUD.update(id=comment_id, input_data=comment)
        return await CommentCRUD.retrieve(id=comment_id)

    @staticmethod
    async def delete(comment_id: UUID) -> None:
        await CommentCRUD.delete(id=comment_id)

    @staticmethod
    async def like(comment_id: UUID, user_id: UUID) -> None:
        try:
            comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
            data = ReactionTypeSchema(reaction_type=ReactionType.LIKE)
            await CommentReactionCRUD.update(id=comment_reaction.id, input_data=data)
        except NotFoundException:
            data = ReactionCreateSchema(comment_id=comment_id, owner_id=user_id, reaction_type=ReactionType.LIKE)
            await CommentReactionCRUD.create(data)

    @staticmethod
    async def dislike(comment_id: UUID, user_id: UUID) -> None:
        try:
            comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
            data = ReactionTypeSchema(reaction_type=ReactionType.DISLIKE)
            await CommentReactionCRUD.update(id=comment_reaction.id, input_data=data)
        except NotFoundException:
            data = ReactionCreateSchema(comment_id=comment_id, owner_id=user_id, reaction_type=ReactionType.DISLIKE)
            await CommentReactionCRUD.create(data)

    @staticmethod
    async def unlike(comment_id: UUID, user_id: UUID) -> None:
        comment_reaction = await CommentReactionCRUD.retrieve(comment_id=comment_id, owner_id=user_id)
        await CommentReactionCRUD.delete(id=comment_reaction.id)
