from datetime import datetime

from pydantic import BaseModel, Field, model_validator


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
    current_password: str
    new_password: str = Field(min_length=8)
    new_password_confirm: str = Field(min_length=8)

    @model_validator(mode="after")
    def validate_passwords(self):
        new_password = self.new_password
        if new_password != self.new_password_confirm:
            raise ValueError("passwords do not match")
        if self.current_password == new_password:
            raise ValueError("your new password can not be like your current password")
        return self
