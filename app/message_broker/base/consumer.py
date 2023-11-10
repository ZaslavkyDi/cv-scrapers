import asyncio
import typing

from aio_pika import Channel
from aio_pika.abc import AbstractIncomingMessage

from app.message_broker.base.connection import get_rabbitmq_channel, get_rabbitmq_connection
from app.message_broker.congif import get_rabbitmq_settings


async def consume_events(
    queue_name: str,
    routing_keys: tuple[str, ...],
    callback: typing.Callable[[AbstractIncomingMessage], typing.Any],
    enable_x_dead_letter: bool,
) -> None:
    channel: Channel = await get_rabbitmq_channel()
    dlq_name = f"{queue_name}.dlq"

    await channel.set_qos(prefetch_count=get_rabbitmq_settings().channel_prefetch_count)  # type: ignore

    # Declare DLQ queue for failed letters
    await channel.declare_queue(
        dlq_name,
        durable=True,
        arguments={"x-max-length": get_rabbitmq_settings().dlq_max_length}
    )

    queue_dead_letter_params: dict[str, typing.Any] | None = None
    if enable_x_dead_letter:
        queue_dead_letter_params = _generate_queue_dead_letter_queue_params(queue_name)

    queue = await channel.declare_queue(
        queue_name,
        durable=True,
        arguments=queue_dead_letter_params
    )

    await asyncio.gather(
        *[
            queue.bind(  # type: ignore
                exchange=get_rabbitmq_settings().exchange_name, routing_key=key
            )
            for key in routing_keys
        ]
    )
    await queue.consume(callback)


def _generate_queue_dead_letter_queue_params(queue_name: str) -> dict[str, typing.Any]:
    return {
        "x-dead-letter-exchange": get_rabbitmq_settings().dlq_exchange_name,
        "x-dead-letter-routing-key": queue_name,
    }
