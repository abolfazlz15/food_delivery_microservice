from pydantic import BaseModel


class NotificationOTPSchema(BaseModel):
    email: str
    otp: str
    message: str
