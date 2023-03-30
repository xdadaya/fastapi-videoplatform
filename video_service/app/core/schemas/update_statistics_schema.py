from pydantic import BaseModel


class UpdateSchema(BaseModel):
    user_id: str
    comments_amount: int = 0
    videos_amount: int = 0
    total_rating: int = 0
    total_text_length: int = 0
