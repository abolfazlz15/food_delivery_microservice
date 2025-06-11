from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base
from src.model.base_model import BaseModel


class NotificationConfig(BaseModel, Base):
    __tablename__ = "notification_configs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    configuration: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )
