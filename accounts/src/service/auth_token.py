import uuid
from datetime import datetime, timedelta, timezone

import jwt

from src.config.base_config import settings
from src.repository_interface.auth_token_repository_interface import (
    AuthTokenRepositoryInterface,
)


class AuthTokenService:
    def __init__(self, auth_repository: AuthTokenRepositoryInterface) -> None:
        self.auth_repository = auth_repository

    async def create_refresh_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        """Generate a refresh token."""
        jti = uuid.uuid4()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=30))
        to_encode.update({"exp": expire, "jti": str(jti)})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        await self.auth_repository.create_token(jti, int(data["sub"]))
        return encoded_jwt

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
