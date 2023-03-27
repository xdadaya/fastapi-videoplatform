from uuid import UUID

from pydantic import BaseModel, Field

from app.core.utils import OID, MongoModel


class UserStatisticsBaseScheme(BaseModel):
    user_id: UUID
    comments_amount: int
    videos_amount: int
    avg_rating: float
    avg_text_length: float
    avg_comments_per_video: float


class UserStatisticsDBSchema(MongoModel, UserStatisticsBaseScheme):
    id: OID = Field(alias='_id')
