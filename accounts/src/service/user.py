from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import UserRepository
from src.schema.user import ChangePasswordInSchema, UserInDBSchema
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
