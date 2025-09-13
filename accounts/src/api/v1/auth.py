from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.common.http_response.response_handler import SuccessResult
from src.common.http_response.success_response import SuccessResponse
from src.config.base_config import settings
from src.depends import get_auth_token_repository, get_user_repository
from src.repository_interface.auth_token_repository_interface import (
    AuthTokenRepositoryInterface,
)
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.token import TokenSchema
from src.service.auth import AuthService
from src.service.auth_token import AuthTokenService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/swagger/login/",
    response_model=TokenSchema,
    name="auth:login",
)
async def swagger_login_router(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_repository: Annotated[
        AuthTokenRepositoryInterface, Depends(get_auth_token_repository)
    ],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> TokenSchema:
    """swagger UI login endpoint"""
    user = await AuthService(user_repository).authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthTokenService.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.access_token_lifetime),
    )
    refresh_token = await AuthTokenService(auth_repository).create_refresh_token(
        data={"sub": str(user.id), "user_role": user.role.name},
        expires_delta=timedelta(days=settings.refresh_token_lifetime),
    )

    return TokenSchema(
        refresh_token=refresh_token,
        access_token=access_token,
        token_type="bearer",
    )


@router.post(
    "/login/",
    response_model=SuccessResponse[TokenSchema],
    name="auth:login",
)
async def login_router(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_repository: Annotated[
        AuthTokenRepositoryInterface, Depends(get_auth_token_repository)
    ],
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[TokenSchema]:
    user = await AuthService(user_repository).authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthTokenService.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.access_token_lifetime),
    )
    refresh_token = await AuthTokenService(auth_repository).create_refresh_token(
        data={"sub": str(user.id), "user_role": user.role.name},
        expires_delta=timedelta(days=settings.refresh_token_lifetime),
    )

    tokens = TokenSchema(
        refresh_token=refresh_token,
        access_token=access_token,
        token_type="bearer",
    )

    return SuccessResult[TokenSchema](
        message="user authenticate successfully",
        status_code=status.HTTP_200_OK,
        data=tokens,
    ).to_response_model(request=request)
