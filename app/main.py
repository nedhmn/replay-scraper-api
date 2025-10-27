import contextlib
import logging
from collections.abc import AsyncGenerator

import aioboto3
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.main import authenticated_router, public_router
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

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing aioboto3 session")
    app.state.aioboto3_session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    yield

    logger.info("Cleaning up aioboto3 session")
    app.state.aioboto3_session = None


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.state.limiter = limiter

# Exception handlers
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(ValueError, value_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, general_exception_handler)

# Middleware stack
app.add_middleware(SlowAPIMiddleware)
app.middleware("http")(metrics_middleware)
app.middleware("http")(request_id_middleware)
app.middleware("http")(security_headers_middleware)

app.include_router(public_router, prefix="/api/v1")
app.include_router(authenticated_router, prefix="/api/v1")
