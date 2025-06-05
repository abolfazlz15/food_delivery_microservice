import aio_pika
from aio_pika.abc import AbstractChannel


class RabbitMQManager:
    """Manages RabbitMQ connections and channels for publishing messages."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: AbstractChannel | None = None

    async def ensure_connection(self) -> AbstractChannel:
        """Ensure the connection and channel are ready."""
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
        return self.channel

    async def publish(self, queue_name: str, message_body: bytes) -> None:
        """Ensure queue exists and publish a message."""

        await self.channel.declare_queue(queue_name, durable=True)

        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=queue_name,
        )

    async def close_connection(self) -> None:
        """Close the connection to RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
