from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.security.password_hash import verify_password
from src.config.base_config import settings
from src.depends import get_user_repository
from src.repository.user import UserRepository
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.user import UserFullDataSchema, UserReadSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/swagger/login")


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> UserFullDataSchema | None:
    user_dict = await UserRepository(session).get_user_by_email(email=email)
    if not user_dict:
        return None
    user = UserFullDataSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
        role=user_dict.role,
    )
    if not verify_password(password, user.password):
        return None
    return user


async def get_current_user(
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserFullDataSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise credentials_exception
    user_test = await user_repository.get_user_detail_by_id(id=int(user_id))
    user_test = UserFullDataSchema(
        id=user_test.id,
        fullname=user_test.fullname,
        email=user_test.email,
        is_active=user_test.is_active,
        created_at=user_test.created_at,
        updated_at=user_test.updated_at,
        password=user_test.password,
        role=user_test.role,
    )
    if user_test is None:
        raise credentials_exception
    return user_test


async def get_current_active_user(
    current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> UserReadSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
