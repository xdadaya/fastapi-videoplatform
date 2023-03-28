import json
from typing import Any

import aio_pika

from app.core.config import get_settings


settings = get_settings()


async def publish(data: dict[Any, Any], send_method: str) -> None:
    connection = await aio_pika.connect(settings.broker_url)

    async with connection:
        routing_key = settings.RB_QUEUE_NAME
        channel = await connection.channel()
        data = {'method': send_method, 'data': data}
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(data).encode()),
            routing_key=routing_key,
        )
