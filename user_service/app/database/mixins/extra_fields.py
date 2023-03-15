from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class ExtraFields:
    @declared_attr
    def is_deleted(cls):
        return Column(Boolean, default=False)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
