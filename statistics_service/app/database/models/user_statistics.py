from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

from app.core.utils import OID, MongoModel


class UserStatisticsCreateScheme(BaseModel):
    user_id: UUID
    comments_amount: Optional[int] = 0
    videos_amount: Optional[int] = 0
    total_rating: Optional[int] = 0
    total_text_length: Optional[int] = 0


class UserStatisticsUpdateScheme(BaseModel):
    comments_amount: int
    videos_amount: int
    total_rating: int
    total_text_length: int


class UserStatisticsBaseScheme(BaseModel):
    user_id: UUID
    comments_amount: int
    videos_amount: int
    total_rating: int
    total_text_length: int


class UserStatisticsResponseScheme(BaseModel):
    user_id: UUID
    comments_amount: int
    avg_rating: float
    avg_text_length: float
    avg_comments_per_video: float


class UserStatisticsDBScheme(MongoModel, UserStatisticsBaseScheme):
    id: OID = Field(alias='_id')
