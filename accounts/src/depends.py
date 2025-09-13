from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from src.repository.auth_token import AuthTokenRepository
from src.repository.user import UserRepository
from src.repository_interface.auth_token_repository_interface import (
    AuthTokenRepositoryInterface,
)
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.user import UserFullDataSchema
from src.service.auth import AuthService, oauth2_scheme


def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepositoryInterface:
    return UserRepository(db_session)


def get_auth_token_repository(
    db_session: Annotated[AsyncSession, Depends(get_db)],
) -> AuthTokenRepositoryInterface:
    return AuthTokenRepository(db_session)


def get_auth_service(
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository)


async def get_current_user(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserFullDataSchema:
    return await auth_service.get_current_user(token)


async def get_current_active_user(
    current_user: Annotated[UserFullDataSchema, Depends(get_current_user)],
) -> UserFullDataSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
