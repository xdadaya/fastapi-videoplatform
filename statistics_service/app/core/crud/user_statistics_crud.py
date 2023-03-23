from uuid import UUID
from bson import Binary

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from app.database.models. user_statistics import UserStatisticsBaseScheme, UserStatisticsDBScheme
from app.core.config import get_settings
from app.core.crud.base_crud_mixin import CRUDMixin


settings = get_settings()


class UserStatisticsCRUD(CRUDMixin):
    db_name: str = settings.DB_NAME
    Collection: str = settings.DB_STATISTICS_COLLECTION
    CreateScheme: BaseModel = UserStatisticsBaseScheme
    RetrieveDBScheme: BaseModel = UserStatisticsDBScheme