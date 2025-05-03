import uuid

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.config.database import Base
from src.model.base_model import BaseModel


class AuthToken(BaseModel, Base):
    """
    Store the JTI (JWT ID) of active tokens to enable token revocation checks.

    Note: Refresh tokens will be removed automatically upon revocation or expiration.
    """

    __tablename__ = "auth_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    jti: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        index=True,
        default=uuid.uuid4,
        unique=True,
    )
    user_id: Mapped[int]
