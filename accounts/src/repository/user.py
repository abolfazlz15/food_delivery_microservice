import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.user import User
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.user import UserUpdateSchema


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by email."""
        if result := await self.session.scalar(
            sa.select(User).where(User.email == email)
        ):
            return result
        return None

    async def get_user_detail_by_id(self, id: int) -> User | None:
        if result := await self.session.scalar(sa.select(User).where(User.id == id)):
            return result
        return None

    async def update_user(
        self, user_id: int, user_data: UserUpdateSchema
    ) -> User | None:

        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return await self.get_user_detail_by_id(user_id)
        stmt = (
            sa.update(User)
            .where(User.id == user_id)
            .values(update_data)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        updated_user = result.scalar_one_or_none()
        if updated_user:
            await self.session.commit()
        return updated_user
