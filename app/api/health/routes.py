from fastapi import APIRouter

from app.api.health.models import HealthCheckResponse

router = APIRouter()


@router.get("", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
