from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base
from app.database.mixins.extra_fields import ExtraFields
from app.database.models.enums.reaction_type_enum import ReactionType


class CommentReaction(Base, ExtraFields):
    __tablename__ = "comment_reactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    comment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=False,
    )
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    reaction_type = Column(Enum(ReactionType), nullable=False)
    comment = relationship("Comment", backref="reactions")
