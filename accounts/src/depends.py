from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.repository.auth_token import AuthTokenRepository
from src.repository.user import UserRepository
from src.repository_interface.auth_token_repository_interface import (
    AuthTokenRepositoryInterface,
)
from src.repository_interface.user_repository_interface import UserRepositoryInterface


def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryInterface:
    return UserRepository(db_session)


def get_auth_token_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> AuthTokenRepositoryInterface:
    return AuthTokenRepository(db_session)
