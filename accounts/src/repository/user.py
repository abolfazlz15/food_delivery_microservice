import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by email."""
        if result := await self.session.scalar(
            sa.select(User).where(User.email == email)
        ):
            return result
        return None

    async def get_all_user_data_by_id(self, id: int) -> User | None:
        if result := await self.session.scalar(sa.select(User).where(User.id == id)):
            return result
        return None


    async def update_user(self, user_id: int, **kwargs) -> User | None:
        """
        Update a user's fields.
        
        Args:
            user_id: ID of the user to update.
            kwargs: Fields to update (e.g., fullname, email).
        
        Returns:
            The updated user object or None if the user doesn't exist.
        """
        stmt = sa.update(User).where(User.id == user_id).values(**kwargs).returning(User)
        result = await self.session.execute(stmt)
        updated_user = result.scalar_one_or_none()
        if updated_user:
            await self.session.commit()
        return updated_user