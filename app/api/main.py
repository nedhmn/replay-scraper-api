from fastapi import APIRouter, Depends

from app.api.health.routes import router as health_router
from app.api.replays.routes import router as replays_router
from app.api.replays.scrape.routes import router as scrape_router
from app.core.auth import verify_api_key

public_router = APIRouter()
authenticated_router = APIRouter(dependencies=[Depends(verify_api_key)])

public_router.include_router(health_router, prefix="/health", tags=["utils"])
authenticated_router.include_router(replays_router, prefix="/replays", tags=["replays"])
authenticated_router.include_router(
    scrape_router, prefix="/replays/scrape", tags=["replays"]
)
