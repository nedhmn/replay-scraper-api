from fastapi import APIRouter

from app.api.health.routes import router as health_router
from app.api.replays.scrape.routes import router as scrape_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["utils"])
router.include_router(scrape_router, prefix="/replays/scrape", tags=["replays"])
