from typing import Any
from src.common.http_response.error_response import ErrorCodes, ErrorResponse


class AppBaseException(Exception):
    def __init__(
        self,
        *,
        code: ErrorCodes,
        message: str,
        status_code: int = 400,
        data: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data or {}

    def to_response_model(self, path: str = "") -> ErrorResponse:
        return ErrorResponse(
            code=self.code,
            message=self.message,
            status=self.status_code,
            path=path,
            data=self.data,
        )
class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict[str, Any], message: str = "Entity not found"):
        super().__init__(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            message=message,
            status_code=404,
            data=data,
        )
