from pydantic import BaseModel


class SMTPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str