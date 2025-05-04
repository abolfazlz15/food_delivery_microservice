import uuid
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.auth_token import AuthTokenRepository
from src.config.base_config import Settings
# from src.repository.token_repository import TokenRepository


class AuthTokenService:
    settings = Settings()

    @classmethod
    async def create_refresh_token(
        cls, session: AsyncSession, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """Generate a refresh token."""
        jti = uuid.uuid4()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=30))
        to_encode.update({"exp": expire, "jti": str(jti)})
        encoded_jwt = jwt.encode(
            to_encode, cls.settings.secret_key, algorithm=cls.settings.algorithm
        )
        await AuthTokenRepository(session).create_token(jti, int(data["sub"]))
        return encoded_jwt

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, cls.settings.secret_key, algorithm=cls.settings.algorithm
        )
