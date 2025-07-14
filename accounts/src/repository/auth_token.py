from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.auth_token import AuthToken
from src.repository_interface.auth_token_repository_interface import (
    AuthTokenRepositoryInterface,
)


class AuthTokenRepository(AuthTokenRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token_by_jti(self, jti: UUID) -> AuthToken | None:
        if auth_token_obj := await self.session.scalar(
            sa.select(
                AuthToken.jti,
                AuthToken.user_id,
            ).where(
                AuthToken.jti == jti,
            )
        ):
            return auth_token_obj
        return None

    async def create_token(self, jti: UUID, user_id: int) -> AuthToken:
        auth_token_obj = AuthToken(
            user_id=user_id,
            jti=jti,
        )
        self.session.add(auth_token_obj)
        await self.session.commit()
        return auth_token_obj
