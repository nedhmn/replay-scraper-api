from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import S3ServiceDep
from app.api.replays.models import ReplayListParams, ReplayListResponse
from app.api.replays.services import get_replay_service, list_replays_service
from app.core.models import ReplayData

router = APIRouter()


@router.get("", response_model=ReplayListResponse)
async def list_replays(
    params: Annotated[ReplayListParams, Query()],
    s3_service: S3ServiceDep,
) -> ReplayListResponse:
    return await list_replays_service(
        s3_service=s3_service,
        page_size=params.page_size,
        after=params.after,
    )


@router.get("/{replay_id}", response_model=ReplayData)
async def get_replay(
    replay_id: str,
    s3_service: S3ServiceDep,
) -> ReplayData:
    return await get_replay_service(s3_service=s3_service, replay_id=replay_id)
