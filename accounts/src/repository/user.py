import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by email."""
        if result := await self.session.scalar(sa.select(User).where(User.email == email)):
            return result
        return None
