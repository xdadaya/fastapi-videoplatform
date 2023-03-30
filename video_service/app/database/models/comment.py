from uuid import uuid4

from sqlalchemy import Column, String, select, func, ForeignKey, Integer
from sqlalchemy.orm import column_property, joinedload
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base
from app.database.mixins.extra_fields import ExtraFields
from app.database.models.comment_reaction import CommentReaction
from app.database.models.enums.reaction_type_enum import ReactionType


class Comment(Base, ExtraFields):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    text = Column(String(256))
    owner_id = Column(UUID(as_uuid=True))
    video_id = Column(
        UUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    likes_amount = column_property(
        select(func.count(CommentReaction.id))
        .where(
            CommentReaction.comment_id == id,
            CommentReaction.reaction_type == ReactionType.LIKE,
        )
        .options(joinedload("comments.c.reactions"))
        .scalar_subquery()
    )
    dislikes_amount = column_property(
        select(func.count(CommentReaction.id))
        .where(
            CommentReaction.comment_id == id,
            CommentReaction.reaction_type == ReactionType.DISLIKE,
        )
        .options(joinedload("comments.c.reactions"))
        .scalar_subquery()
    )
    rating = column_property(
        cast(likes_amount, Integer) - cast(dislikes_amount, Integer)
    )
