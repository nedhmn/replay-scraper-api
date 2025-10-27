import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.middleware import get_request_id

logger = logging.getLogger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    request_id = get_request_id()
    logger.warning(
        "Validation error path=%s request_id=%s errors=%s",
        request.url.path,
        request_id,
        exc.errors(),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "request_id": request_id,
        },
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    request_id = get_request_id()
    logger.warning(
        "Value error path=%s request_id=%s error=%s",
        request.url.path,
        request_id,
        str(exc),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": str(exc),
            "request_id": request_id,
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    request_id = get_request_id()

    if exc.status_code >= 500:
        logger.error(
            "HTTP error path=%s request_id=%s status=%d detail=%s",
            request.url.path,
            request_id,
            exc.status_code,
            exc.detail,
        )
    else:
        logger.warning(
            "HTTP error path=%s request_id=%s status=%d detail=%s",
            request.url.path,
            request_id,
            exc.status_code,
            exc.detail,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "request_id": request_id,
        },
        headers=exc.headers,
    )


async def general_exception_handler(request: Request, _exc: Exception) -> JSONResponse:
    request_id = get_request_id()
    logger.exception(
        "Unhandled exception path=%s request_id=%s",
        request.url.path,
        request_id,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
        },
    )
