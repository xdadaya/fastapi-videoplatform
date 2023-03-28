import asyncio
from dotenv import dotenv_values

import aio_pika

from app.database.db_utils import connect
from app.services.message_service import MessageService
from app.core.config import get_settings


settings = get_settings()


async def main() -> None:
    connection = await aio_pika.connect_robust(settings.broker_url)
    queue_name = settings.RB_QUEUE_NAME
    await connect()
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await MessageService.process_message(message.body)


if __name__ == "__main__":
    asyncio.run(main())
