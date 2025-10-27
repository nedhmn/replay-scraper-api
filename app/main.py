import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.main import router
from app.core.config import settings
from app.core.exceptions import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    value_error_handler,
)
from app.core.logging import configure_logging
from app.core.middleware import (
    metrics_middleware,
    request_id_middleware,
    security_headers_middleware,
)

configure_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.PROJECT_NAME)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ValueError, value_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, general_exception_handler)

# Middleware stack
app.middleware("http")(metrics_middleware)
app.middleware("http")(request_id_middleware)
app.middleware("http")(security_headers_middleware)

app.include_router(router, prefix="/api/v1")
