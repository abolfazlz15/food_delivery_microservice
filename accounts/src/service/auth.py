from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.base_config import Settings
from src.config.database import get_db
from src.repository.user import UserRepository
from src.schema.user import UserFullDataSchema, UserInDBSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
settings = Settings()


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> UserInDBSchema | None:
    user_dict = await UserRepository(session).get_user_by_email(email=email)
    if not user_dict:
        return None
    user = UserInDBSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
    )
    if not verify_password(password, user.password):
        return None
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches its hashed counterpart.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.
    """
    return pwd_context.hash(password)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDBSchema:
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
    user_dict = await UserRepository(session).get_all_user_data_by_id(id=user_id)
    user = UserInDBSchema(
        id=user_dict.id,
        fullname=user_dict.fullname,
        email=user_dict.email,
        is_active=user_dict.is_active,
        created_at=user_dict.created_at,
        updated_at=user_dict.updated_at,
        password=user_dict.password,
    )
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserFullDataSchema, Depends(get_current_user)],
) -> UserInDBSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
