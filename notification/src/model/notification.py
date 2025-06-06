from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.common.enum.notification_type_enum import NotificationTypeEnum
from src.config.database import Base
from src.model.base_model import BaseModel


class Notification(BaseModel, Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    title: Mapped[str]
    subject: Mapped[str] = mapped_column(
        nullable=True,
    )
    body: Mapped[str] = mapped_column(Text)
    type: Mapped[NotificationTypeEnum]
    is_active: Mapped[bool] = mapped_column(
        default=False,
    )
