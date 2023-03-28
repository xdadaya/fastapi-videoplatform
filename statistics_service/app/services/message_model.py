from typing import Optional

from pydantic import BaseModel


class MessageBody(BaseModel):
    user_id: str
    videos_amount: Optional[int] = 0
    comments_amount: Optional[int] = 0
    total_text_length: Optional[int] = 0
    total_rating: Optional[int] = 0


class MessageScheme(BaseModel):
    method: str
    data: MessageBody
