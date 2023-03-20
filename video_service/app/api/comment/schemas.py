from uuid import UUID

from pydantic import BaseModel


class CommentCreateRequest(BaseModel):
    text: str


class CommentCreateSchema(CommentCreateRequest):
    id: UUID
    owner_id: UUID
    video_id: UUID


class CommentSerializer(BaseModel):
    id: UUID
    text: str
    owner_id: UUID
    video_id: UUID
    likes_amount: int
    dislikes_amount: int

    class Config:
        orm_mode = True


class ReactionTypeSchema(BaseModel):
    reaction_type: str


class ReactionCreateSchema(BaseModel):
    owner_id: UUID
    comment_id: UUID
    reaction_type: str
