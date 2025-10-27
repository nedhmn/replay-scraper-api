from typing import Annotated
from urllib.parse import parse_qs, urlparse

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import S3ServiceDep
from app.api.replays.models import ReplayData
from app.api.replays.scrape.models import ReplayUrlRequest, ValidatedReplayData
from app.api.replays.scrape.services import scrape_replay

router = APIRouter()


async def validate_and_clean_replay_url(
    request: ReplayUrlRequest,
) -> ValidatedReplayData:
    try:
        parsed = urlparse(request.replay_url)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid URL format",
        ) from exc

    if "duelingbook.com" not in parsed.netloc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL must be from duelingbook.com domain",
        )

    if parsed.path != "/replay":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL path must be /replay",
        )

    query_params = parse_qs(parsed.query)

    if "id" not in query_params:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL must contain 'id' query parameter",
        )

    id_value = query_params["id"][0]

    # Clean the id by removing userId prefix if present (e.g., "21733-2178594" → "2178594")
    if "-" in id_value:
        cleaned_id_str = id_value.split("-")[-1]
    else:
        cleaned_id_str = id_value

    try:
        replay_id = int(cleaned_id_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid replay ID format: '{id_value}'. ID must be an integer.",
        ) from exc

    cleaned_url = f"https://www.duelingbook.com/replay?id={replay_id}"

    return ValidatedReplayData(cleaned_url=cleaned_url, replay_id=replay_id)


@router.post("", response_model=ReplayData)
async def scrape_replay_route(
    validated: Annotated[ValidatedReplayData, Depends(validate_and_clean_replay_url)],
    s3_service: S3ServiceDep,
) -> ReplayData:
    replay_id_str = str(validated.replay_id)

    cached_replay = await s3_service.get_replay(replay_id_str)
    if cached_replay is not None:
        return cached_replay

    replay_data = await scrape_replay(validated.cleaned_url, replay_id_str)

    await s3_service.save_replay(replay_id_str, replay_data)

    return replay_data
