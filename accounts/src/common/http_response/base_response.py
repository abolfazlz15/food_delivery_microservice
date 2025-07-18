from datetime import datetime

from pydantic import BaseModel, PositiveInt


class BaseResponse(BaseModel):
    status: PositiveInt
    message: str
    timestamp: datetime
    path: str
