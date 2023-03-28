import json
from typing import Any

import aio_pika


async def publish(data: dict[Any, Any], send_method: str) -> None:
    connection = await aio_pika.connect("amqp://guest:guest@rabbitmq:5672//")

    async with connection:
        routing_key = "test_queue"
        channel = await connection.channel()
        data = {'method': send_method, 'data': data}
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode()),
            routing_key=routing_key,
        )
