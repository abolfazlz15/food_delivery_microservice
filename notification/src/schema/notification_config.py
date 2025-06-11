from pydantic import BaseModel, ConfigDict

from src.schema.email import EmailConfig


class BaseConfig(BaseModel):
    email: EmailConfig = EmailConfig()

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )
