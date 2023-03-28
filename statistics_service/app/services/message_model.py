from typing import Optional

from pydantic import BaseModel


class MessageBody(BaseModel):
    user_id: str
    videos_amount: int = 0
    comments_amount: int = 0
    total_text_length: int = 0
    total_rating: int = 0


class MessageScheme(BaseModel):
    method: str
    data: MessageBody
