from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
from app.core.utils import OID


class CRUDMixin:
    db_name: str
    Collection: str
    CreateScheme: Any
    RetrieveDBScheme: Any

    @classmethod
    async def create(cls, conn: AsyncIOMotorClient, data: "CreateScheme") -> None:
        doc = data.dict()
        await conn[cls.db_name][cls.Collection].insert_one(doc)

    @classmethod
    async def retrieve(cls, conn: AsyncIOMotorClient, **kwargs):
        return await conn[cls.db_name][cls.Collection].find_one(kwargs)

    @classmethod
    async def list(cls, conn: AsyncIOMotorClient, **kwargs):
        result = []
        rows = conn[cls.db_name][cls.Collection].find(kwargs)
        async for row in rows:
            result.append(cls.RetrieveDBScheme(**row))
        return result

    @classmethod
    async def update(cls, conn: AsyncIOMotorClient, _id: OID, **kwargs) -> None:
        await conn[cls.db_name][cls.Collection].update_one({"_id": _id}, {"$set": kwargs})

    @classmethod
    async def delete(cls, conn: AsyncIOMotorClient, _id: OID) -> None:
        await conn[cls.db_name][cls.Collection].delete_one({"_id": _id})
