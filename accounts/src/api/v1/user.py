from fastapi import APIRouter, Depends, status

from src.config.base_config import Settings
from src.schema.user import UserFullDataSchema, UserInDBSchema
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
