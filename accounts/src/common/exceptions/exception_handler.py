from fastapi import Request
from fastapi.responses import JSONResponse, Response

from src.common.exceptions.exceptions import AppBaseException


async def handle_app_exception(request: Request, exc: AppBaseException) -> Response:
    error_model = exc.to_response_model(path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": error_model.model_dump(mode="json")},
    )
