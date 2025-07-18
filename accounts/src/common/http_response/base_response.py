from pydantic import BaseModel, PositiveInt


class BaseResponse(BaseModel):
    status: PositiveInt
    message: str
    path: str
