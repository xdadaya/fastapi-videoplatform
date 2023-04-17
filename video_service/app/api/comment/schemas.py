from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.fastapi.user_data import OwnerSerializer


class CommentCreateRequest(BaseModel):
    text: str


class CommentCreateSchema(CommentCreateRequest):
    id: UUID
    owner_id: UUID
    video_id: UUID


class CommentSerializer(BaseModel):
    id: UUID
    text: str
    owner: OwnerSerializer
    video_id: UUID
    likes_amount: int
    dislikes_amount: int
    rating: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentListResponse(BaseModel):
    page_number: int
    page_size: int
    total_pages: int
    items: list[CommentSerializer]


class ReactionTypeSchema(BaseModel):
    reaction_type: str


class ReactionCreateSchema(BaseModel):
    owner_id: UUID
    comment_id: UUID
    reaction_type: str
