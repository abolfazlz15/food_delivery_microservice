from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi import Request

from src.common.http_response.success_response import SuccessResponse


T = TypeVar("T")


@dataclass
class SuccessResult(Generic[T]):
    def __init__(
        self,
        *,
        message: str = "Operation successful",
        status_code: int = 200,
        data: T | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.data = data

    def to_response_model(self, request: Request) -> SuccessResponse[T]:
        return SuccessResponse[T](
            message=self.message,
            status=self.status_code,
            data=self.data,
            path=self._get_path(request),
        )

    @staticmethod
    def _get_path(request: Request) -> str:
        return request.url.path
