from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.http_response.response_handler import SuccessResult
from src.common.http_response.success_response import SuccessResponse
from src.config.base_config import settings
from src.config.database import get_db
from src.schema.token import TokenSchema
from src.service.auth import authenticate_user
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
    db: AsyncSession = Depends(get_db),
) -> TokenSchema:
    """swagger UI login endpoint"""
    user = await authenticate_user(db, form_data.username, form_data.password)
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
    refresh_token = await AuthTokenService.create_refresh_token(
        session=db,
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
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse[TokenSchema]:
    user = await authenticate_user(db, form_data.username, form_data.password)
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
    refresh_token = await AuthTokenService.create_refresh_token(
        session=db,
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
