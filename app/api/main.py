from fastapi import APIRouter

from app.api.health.routes import router as health_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["utils"])
