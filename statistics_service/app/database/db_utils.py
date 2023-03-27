from motor.motor_asyncio import AsyncIOMotorClient
from app.database.db import db
from app.core.config import get_settings


settings = get_settings()


async def connect():
    mongo_url = settings.database_url
    db.client = AsyncIOMotorClient(mongo_url)


async def close_connection():
    db.client.close()
