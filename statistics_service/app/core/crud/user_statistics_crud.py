from uuid import UUID
from bson import Binary

from motor.motor_asyncio import AsyncIOMotorClient

from app.database.models. user_statistics import UserStatisticsBaseScheme, UserStatisticsDBSchema
from app.core.config import get_settings


settings = get_settings()


class UserStatisticsCRUD:
    db_name: str = settings.DB_NAME
    collection: str = settings.DB_STATISTICS_COLLECTION

    @classmethod
    async def create(cls, conn: AsyncIOMotorClient, data: UserStatisticsBaseScheme) -> None:
        doc = data.dict()
        doc['user_id'] = Binary.from_uuid(doc['user_id'])
        await conn[cls.db_name][cls.collection].insert_one(doc)

    @classmethod
    async def retrieve(cls, conn: AsyncIOMotorClient, user_id: UUID):
        result = await conn[cls.db_name][cls.collection].find_one({'user_id': Binary.from_uuid(user_id)})
        return result

    @classmethod
    async def update(cls, conn: AsyncIOMotorClient, data: UserStatisticsBaseScheme) -> None:
        doc = data.dict()
        doc['user_id'] = Binary.from_uuid(doc['user_id'])
        await conn[cls.db_name][cls.collection].update_one({'user_id': doc['user_id']}, {'$set': {
            'comments_amount': doc['comments_amount'],
            'videos_amount': doc['videos_amount'],
            'avg_rating': doc['avg_rating'],
            'avg_text_length': doc['avg_text_length'],
            'avg_comments_per_video': doc['avg_comments_per_video']
        }})

    @classmethod
    async def delete(cls, conn: AsyncIOMotorClient, user_id: UUID) -> None:
        await conn[cls.db_name][cls.collection].delete_one({'user_id': Binary.from_uuid(user_id)})
