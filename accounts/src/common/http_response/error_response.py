from typing import Any

from src.common.enum.error_code import ErrorCodes
from src.common.http_response.base_response import BaseResponse


class ErrorResponse(BaseResponse):

    code: ErrorCodes
    data: dict[str, Any] | None = None