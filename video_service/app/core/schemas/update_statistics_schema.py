from typing import Optional
from pydantic import BaseModel


class UpdateSchema(BaseModel):
    user_id: str
    comments_amount: Optional[int]
    videos_amount: Optional[int]
    total_rating: Optional[int]
    total_text_length: Optional[int]
