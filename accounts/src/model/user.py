from sqlalchemy.orm import Mapped, mapped_column
from src.common.enum.user_role import UserRoleEnum
from src.config.database import Base
from src.model.base_model import BaseModel


class User(BaseModel, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    fullname: Mapped[str]
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    role: Mapped[UserRoleEnum] = mapped_column(
        default=UserRoleEnum.USER,
    )
