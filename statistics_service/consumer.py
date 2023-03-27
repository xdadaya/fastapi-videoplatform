import asyncio
import json
from uuid import UUID

import aio_pika

from app.core.crud.user_statistics_crud import UserStatisticsCRUD
from app.database.db import get_database
from app.database.db_utils import connect
from app.database.models.user_statistics import UserStatisticsCreateScheme, UserStatisticsUpdateScheme


async def main() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672//")
    queue_name = "test_queue"
    await connect()
    db = await get_database()
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    if body["method"] == "create_stats":
                        data = UserStatisticsCreateScheme(user_id=UUID(body["data"]["user_id"]))
                        await UserStatisticsCRUD.create(db, data)
                    elif body["method"] == "delete_stats":
                        stats = await UserStatisticsCRUD.retrieve(db, user_id=UUID(body["data"]["user_id"]))
                        await UserStatisticsCRUD.delete(db, stats["_id"])
                    elif body["method"] == "update_stats":
                        stats = await UserStatisticsCRUD.retrieve(db, user_id=UUID(body["data"]["user_id"]))
                        print(stats)


if __name__ == "__main__":
    asyncio.run(main())
