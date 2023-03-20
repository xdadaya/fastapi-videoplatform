from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base
from app.database.mixins.extra_fields import ExtraFields


class Category(Base, ExtraFields):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(256), unique=True)
