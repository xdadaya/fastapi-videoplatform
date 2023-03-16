from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserSerializer(BaseModel):
    id: UUID
    username: str
    created_at: datetime

    class Config:
        orm_mode = True
