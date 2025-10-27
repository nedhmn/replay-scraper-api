import logging

import httpx
from anticaptchaofficial.recaptchav3proxyless import (  # type: ignore
    recaptchaV3Proxyless,
)
from fastapi import HTTPException, status
from pydantic import ValidationError

from app.core.config import settings
from app.core.middleware import get_request_id
from app.core.models import ReplayData

logger = logging.getLogger(__name__)


async def solve_recaptcha_v3(url: str) -> str:
    solver = recaptchaV3Proxyless()
    solver.set_verbose(1)
    solver.set_key(settings.ANTICAPTCHA_API_KEY)
    solver.set_website_url(url)
    solver.set_website_key(settings.SITE_KEY)
    solver.set_min_score(0.9)

    g_response: str = solver.solve_and_return_solution()

    # Weirdly, the solver returns "0" when the CAPTCHA fails.
    # ref: https://anti-captcha.com/apidoc/task-types/RecaptchaV3TaskProxyless

    if g_response == "0":
        request_id = get_request_id()
        logger.error(
            "CAPTCHA verification failed url=%s request_id=%s error_code=%s",
            url,
            request_id,
            solver.error_code,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify CAPTCHA. Please try again.",
        )

    return g_response


async def scrape_replay(url: str, replay_id: str) -> ReplayData:
    g_response = await solve_recaptcha_v3(url)

    async with httpx.AsyncClient() as client:
        data_url = f"https://www.duelingbook.com/view-replay?id={replay_id}"
        form_data = {"token": g_response, "recaptcha_version": 3, "master": False}
        response = await client.post(url=data_url, data=form_data)

        replay_data = response.json()

    try:
        return ReplayData.model_validate(replay_data)
    except ValidationError as exc:
        request_id = get_request_id()
        logger.error(
            "Invalid replay response replay_id=%s request_id=%s errors=%s",
            replay_id,
            request_id,
            exc.errors(),
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from DuelingBook.",
        ) from exc
