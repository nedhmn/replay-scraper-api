from fastapi import HTTPException, status

from app.api.replays.models import ReplayData, ReplayListResponse, ReplayPagination
from app.core.s3 import ReplayS3Service


async def get_replay_service(s3_service: ReplayS3Service, replay_id: str) -> ReplayData:
    replay_data = await s3_service.get_replay(replay_id)

    if replay_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Replay {replay_id} not found",
        )

    return replay_data


async def list_replays_service(
    s3_service: ReplayS3Service, page_size: int = 1000, after: str | None = None
) -> ReplayListResponse:
    result = await s3_service.list_replay_ids(page_size=page_size, after=after)

    return ReplayListResponse(
        data=result["replay_ids"],
        pagination=ReplayPagination(
            page_size=page_size,
            next_cursor=result["next_cursor"],
            has_more=result["has_more"],
        ),
    )
