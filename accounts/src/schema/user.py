from datetime import datetime

from pydantic import BaseModel, Field, model_validator, EmailStr, ConfigDict


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


class UserProfileDetailSchema(BaseModel):
    id: int
    fullname: str
    email: str


class UserFullDataSchema(UserProfileDetailSchema):
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    role: str


class UserInDBSchema(UserFullDataSchema):
    password: str


class UserUpdateProfileInDBSchema(BaseModel):
    fullname: str


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
            raise ValueError("passwords do not match")
        if self.current_password == new_password:
            raise ValueError("your new password can not be like your current password")
        return self
