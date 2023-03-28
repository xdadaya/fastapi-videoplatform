import asyncio
from dotenv import dotenv_values

import aio_pika

from app.database.db_utils import connect
from app.services.message_service import MessageService


async def main() -> None:
    config = dotenv_values(".env")
    connection = await aio_pika.connect_robust(f"amqp://guest:guest@{config['RB_HOST']}:{config['RB_PORT']}//")
    queue_name = config['RB_QUEUE_NAME']
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
