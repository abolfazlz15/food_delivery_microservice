from pydantic import BaseModel


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokenSchema(RefreshTokenSchema):
    access_token: str
    token_type: str
