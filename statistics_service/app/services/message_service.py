import json
from uuid import UUID

from app.core.crud.user_statistics_crud import UserStatisticsCRUD
from app.database.db import get_database
from app.database.models.user_statistics import UserStatisticsCreateScheme


class MessageService:
    @staticmethod
    async def process_message(msg: bytes) -> None:
        body = json.loads(msg.decode())
        db = await get_database()
        if body["method"] == "create_stats":
            data = UserStatisticsCreateScheme(user_id=UUID(body["data"]["user_id"]))
            await UserStatisticsCRUD.create(db, data)
        elif body["method"] == "delete_stats":
            await UserStatisticsCRUD.delete(db, user_id=UUID(body["data"]["user_id"]))
        elif body["method"] == "update_stats":
            pass