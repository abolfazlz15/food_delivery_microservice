from src.config.base_config import Settings
from src.config.rabbitmq_config import RabbitMQManager
from src.schema.notification_schema import NotificationOTPSchema


class NotificationService:
    """Service for sending data to notification service."""

    def __init__(self):
        self.__rabbitmq_manager = RabbitMQManager(Settings().rabbitmq_url)

    async def send_otp(self, message_body: NotificationOTPSchema) -> None:
        """Send OTP to the user's email."""
        await self.__rabbitmq_manager.publish(
            queue_name="notification.otp",
            message_body=message_body.model_dump_json().encode("utf-8"),
        )
