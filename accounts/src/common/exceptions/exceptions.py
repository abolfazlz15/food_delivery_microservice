from typing import Any

from fastapi import status

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


class DatabaseOperationException(AppBaseException):
    def __init__(
        self,
        operation: str | None = None,
        message: str | None = None,
        data: dict | None = None,
    ):
        message = f"Failed to perform {operation} operation. {message}"

        super().__init__(
            code=ErrorCodes.DATABASE_ERROR,
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=data,
        )


class InvalidCredentialsException(AppBaseException):
    def __init__(self, data=None, message: str = "Authentication failed"):
        if data is None:
            data = {}
        super().__init__(
            code=ErrorCodes.INVALID_CREDENTIALS,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            data=data,
        )


class EntityNotFoundException(AppBaseException):
    def __init__(self, data: dict[str, Any], message: str = "Entity not found"):
        super().__init__(
            code=ErrorCodes.ENTITY_NOT_FOUND,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            data=data,
        )


class InvalidDataException(AppBaseException):
    def __init__(self, data=None, message: str = "Invalid data"):
        super().__init__(
            code=ErrorCodes.INVALID_PAYLOAD,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            data=data,
        )
