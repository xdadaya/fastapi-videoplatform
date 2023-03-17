from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base
from app.database.mixins.extra_fields import ExtraFields


class Video(Base, ExtraFields):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(256))
    description = Column(String(1024))
    video_url = Column(String(2048))
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

