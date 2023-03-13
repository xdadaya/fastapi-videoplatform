from pydantic import BaseModel
from datetime import datetime


class UserSerializer(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True
