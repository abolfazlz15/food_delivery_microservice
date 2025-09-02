from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from src.common.enum.user_role import UserRoleEnum
from src.common.exceptions.exceptions import InvalidDataException


class UserBaseSchema(BaseModel):
    fullname: str = Field(max_length=255, description="client full name")
    email: EmailStr = Field(description="client unique email address")


class UserUpdateSchema(BaseModel):
    fullname: str | None = Field(
        default=None,
        max_length=255,
        description="update client full name",
    )
    email: EmailStr | None = Field(
        default=None,
        description="update client unique email address",
    )
    password: str | None = Field(
        None, min_length=8, description="update user password confirm"
    )


class UserReadSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="user unique identifier")
    role: UserRoleEnum = Field(description="Role of the user")
    is_active: bool = Field(description="user status")
    created_at: datetime = Field(
        description="date time when user created",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="when user update last time",
    )


class UserFullDataSchema(UserReadSchema):
    password: str


class ChangePasswordInSchema(BaseModel):
    current_password: str = Field(
        description="current user password",
    )
    new_password: str = Field(min_length=8, description="new user password")
    new_password_confirm: str = Field(
        min_length=8, description="new user password confirm"
    )

    @model_validator(mode="after")
    def validate_passwords(self):
        new_password = self.new_password
        if new_password != self.new_password_confirm:
            raise InvalidDataException(
                message="passwords do not match",
            )
        if self.current_password == new_password:
            raise InvalidDataException(
                message="your new password can not be like your current password",
            )
        return self 
