from pydantic import BaseModel, PositiveInt, Field


class BaseResponse(BaseModel):
    status: PositiveInt = Field(examples=[200])
    message: str
    path: str
