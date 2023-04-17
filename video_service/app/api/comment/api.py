from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.comment.schemas import CommentCreateRequest, CommentListSerializer
from app.api.comment.service import CommentService
from shared.fastapi.middleware.middleware import verify_token
from app.core.fastapi.middleware.middleware import is_comment_owner

api = APIRouter(
    prefix="/comments",
)


@api.put(
    "/{comment_id}",
    response_model=CommentListSerializer,
    dependencies=[Depends(is_comment_owner)],
)
async def update_comment(
    comment_id: UUID, comment: CommentCreateRequest
) -> CommentListSerializer:
    return await CommentService.update(comment_id, comment)


@api.delete("/{comment_id}", dependencies=[Depends(is_comment_owner)])
async def delete_comment(comment_id: UUID) -> None:
    await CommentService.delete(comment_id)


@api.post("/{comment_id}/like", status_code=201)
async def like_comment(comment_id: UUID, user_id: UUID = Depends(verify_token)) -> None:
    await CommentService.like(comment_id, user_id)


@api.post("/{comment_id}/dislike", status_code=201)
async def dislike_comment(
    comment_id: UUID, user_id: UUID = Depends(verify_token)
) -> None:
    await CommentService.dislike(comment_id, user_id)


@api.delete("/{comment_id}/unlike", status_code=200)
async def remove_reaction_from_comment(
    comment_id: UUID, user_id: UUID = Depends(verify_token)
) -> None:
    await CommentService.unlike(comment_id, user_id)
