from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.common.enum.notification_report_status_enum import (
    NotificationReportStatusEnum,
)
from src.model.notification import Notification
from src.config.database import Base
from src.model.base_model import BaseModel


class NotificationReport(BaseModel, Base):
    __tablename__ = "Notification_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    user: Mapped[int] = mapped_column(
        index=True,
    )
    notification_id: Mapped[int] = mapped_column(
        ForeignKey(Notification.id),
    )
    result: Mapped[str] = mapped_column(
        nullable=True,
    )
    status: Mapped[NotificationReportStatusEnum] = mapped_column(
        default=NotificationReportStatusEnum.PENDING,
    )
