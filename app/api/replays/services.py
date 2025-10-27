from app.api.replays.models import ReplayListResponse, ReplayPagination
from app.core.s3 import ReplayS3Service


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
