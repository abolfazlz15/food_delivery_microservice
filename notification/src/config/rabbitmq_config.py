import asyncio
import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

class RabbitMQManager:
    """
    Manages a single RobustConnection + channel for publishing _and_ consuming.
    Other classes should call .connect() in startup, then .get_channel() whenever
    they need to declare queues, publish, or start consuming.
    """

    def __init__(self, url: str) -> None:
        self._url = url
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        """
        Establishes a RobustConnection + Channel. If already connected, does nothing.
        """
        async with self._lock:
            if self._connection and not self._connection.is_closed:
                return

            self._connection = await aio_pika.connect_robust(self._url)
            self._channel = await self._connection.channel()

    def get_channel(self) -> AbstractChannel:
        """
        Returns the (already open) channel. Raises if not connected.
        """
        if not self._channel or self._channel.is_closed:
            raise RuntimeError("Channel is not available. Have you called .connect()?")

        return self._channel

    async def close(self) -> None:
        """
        Closes channel & connection. Safe to call multiple times.
        """
        async with self._lock:
            if self._channel and not self._channel.is_closed:
                await self._channel.close()
                self._channel = None

            if self._connection and not self._connection.is_closed:
                await self._connection.close()
                self._connection = None


