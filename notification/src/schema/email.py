from pydantic import BaseModel, Field


class SMTPConfig(BaseModel):
    is_active: bool = Field(default=False)
    host: str | None = Field(default=None)
    port: int | None = Field(default=None)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)


class EmailConfig(BaseModel):
    smtp: SMTPConfig = SMTPConfig()
