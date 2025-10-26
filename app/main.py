import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.main import router

configure_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router, prefix="/api/v1")
