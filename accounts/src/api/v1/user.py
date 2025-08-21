from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from src.common.http_response.success_response import SuccessResponse
from src.common.http_response.response_handler import SuccessResult
from src.depends import get_user_repository
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.user import (
    ChangePasswordInSchema,
    UserFullDataSchema,
    UserReadSchema,
)
from src.service.auth import get_current_active_user
from src.service.user import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    "/detail/",
    response_model=SuccessResponse[UserReadSchema],
    status_code=status.HTTP_200_OK,
    name="user:detail",
)
async def user_detail_router(
    request: Request,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    current_user: UserFullDataSchema = Depends(get_current_active_user),
):
    user_data = await UserService(user_repository).user_detail(current_user)
    return SuccessResult[UserReadSchema](
        message="password change successfully",
        status_code=status.HTTP_200_OK,
        data=user_data,
    ).to_response_model(request=request)


# @router.patch(
#     "/update/",
#     response_model=UserFullDataSchema,
#     status_code=status.HTTP_200_OK,
#     name="user:update",
# )
# async def user_update_router(
#     user_data: UserUpdateSchema,
#     user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
#     current_user: UserInDBSchema = Depends(get_current_active_user),
# ):

#     return await UserRepository(
#         session=db,
#     ).update_user(
#         current_user.id,
#         **user_data.model_dump(),
#     )


@router.patch(
    "/update-password/",
    status_code=status.HTTP_200_OK,
    name="user:change password",
    response_model=SuccessResponse[UserReadSchema],
)
async def change_user_password_router(
    request: Request,
    password_data: ChangePasswordInSchema,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    current_user: UserFullDataSchema = Depends(get_current_active_user),
) -> SuccessResponse[UserReadSchema]:
    user_data = await UserService(user_repository).change_password(
        current_user,
        password_data,
    )
    return SuccessResult[UserReadSchema](
        message="password change successfully",
        status_code=status.HTTP_200_OK,
        data=user_data,
    ).to_response_model(request=request)
