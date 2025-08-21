from src.common.exceptions.exceptions import (
    EntityNotFoundException,
    InvalidCredentialsException,
)
from src.common.security.password_hash import verify_password, hash_password
from src.repository_interface.user_repository_interface import UserRepositoryInterface
from src.schema.user import (
    ChangePasswordInSchema,
    UserFullDataSchema,
    UserReadSchema,
    UserUpdateSchema,
)


class UserService:
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def user_detail(self, current_user: UserFullDataSchema):
        return UserReadSchema(
            id=current_user.id,
            fullname=current_user.fullname,
            email=current_user.email,
            is_active=current_user.is_active,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            role=current_user.role,
        )

    async def change_password(
        self,
        user: UserFullDataSchema,
        password_data: ChangePasswordInSchema,
    ) -> UserReadSchema:
        if not verify_password(password_data.current_password, user.password):
            raise InvalidCredentialsException(message="Password is wrong")

        hashed_new_password = hash_password(password_data.new_password)

        if user_obj := await self.user_repository.update_user(
            user_id=user.id,
            user_data=UserUpdateSchema(password=hashed_new_password),
        ):
            return UserReadSchema.model_validate(user_obj)
        raise EntityNotFoundException(
            data={"user_id": user.id},
            message="user not found",
        )
