from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.user import change_password
from src.config.base_config import Settings
from src.config.database import get_db
from src.repository.user import UserRepository
from src.schema.user import (
    ChangePasswordInSchema,
    UserFullDataSchema,
    UserInDBSchema,
    UserUpdateProfileInDBSchema,
)
from src.service.auth import get_current_active_user

settings = Settings()

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    "/detail/",
    response_model=UserFullDataSchema,
    status_code=status.HTTP_200_OK,
    name="user:detail",
)
async def user_detail_router(
    current_user: UserInDBSchema = Depends(get_current_active_user),
):
    return UserFullDataSchema(
        id=current_user.id,
        fullname=current_user.fullname,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        role=current_user.role,
    )


@router.patch(
    "/update/",
    response_model=UserFullDataSchema,
    status_code=status.HTTP_200_OK,
    name="user:update",
)
async def user_update_router(
    user_data: UserUpdateProfileInDBSchema,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await UserRepository(
        session=db,
    ).update_user(
        current_user.id,
        **user_data.model_dump(),
    )


@router.patch(
    "/change-password/",
    status_code=status.HTTP_200_OK,
    name="user:change password",
)
async def change_user_password_router(
    password_data: ChangePasswordInSchema,
    current_user: UserInDBSchema = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        new_password = await change_password(current_user, password_data, db)
        if not new_password:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "something wrong")
        return {"message": "Your password has been successfully changed"}
    except ValueError as exp:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exp))
