from typing import Generic, TypeVar

from pydantic import BaseModel

from src.common.http_response.base_response import BaseResponse

T = TypeVar("T", bound=BaseModel)


class SuccessResponse(BaseResponse, Generic[T]):
    data: T | None = None
