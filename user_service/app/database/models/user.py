from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base
from app.database.mixins.extra_fields import ExtraFields


class User(Base, ExtraFields):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255))
