from sqlalchemy.ext.asyncio import AsyncSession

from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.repository.user import UserRepository
from src.schema.user import ChangePasswordInSchema, UserFullDataSchema, UserInDBSchema
from src.service.auth import get_password_hash, verify_password


async def change_password(
    user: UserInDBSchema,
    password_data: ChangePasswordInSchema,
    session: AsyncSession,
) -> bool:
    if not verify_password(password_data.current_password, user.password):
        raise ValueError("Old password is incorrect")

    hashed_new_password = get_password_hash(password_data.new_password)
    updated_user = await UserRepository(
        session,
    ).update_user(
        user.id,
        password=hashed_new_password,
    )
    return bool(updated_user)


class UserService:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def user_detail(self, current_user: UserInDBSchema):
        return UserFullDataSchema(
            id=current_user.id,
            fullname=current_user.fullname,
            email=current_user.email,
            is_active=current_user.is_active,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            role=current_user.role,
        )
