from typing import Any

import httpx
from anticaptchaofficial.recaptchav3proxyless import (  # type: ignore
    recaptchaV3Proxyless,
)
from fastapi import HTTPException, status

from app.core.config import settings


def solve_recaptcha_v3(url: str) -> str:
    solver = recaptchaV3Proxyless()
    solver.set_verbose(1)
    solver.set_key(settings.ANTICAPTCHA_API_KEY)
    solver.set_website_url(url)
    solver.set_website_key(settings.SITE_KEY)
    solver.set_min_score(0.9)

    g_response: str = solver.solve_and_return_solution()

    # Weirdly, the solver returns "0" when the CAPTCHA is solved.
    # ref: https://anti-captcha.com/apidoc/task-types/RecaptchaV3TaskProxyless

    if g_response == "0":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify CAPTCHA. Please try again.",
        )

    return g_response


def scrape_replay(url: str, replay_id: str) -> dict[str, Any]:
    g_response = solve_recaptcha_v3(url)

    with httpx.Client() as client:
        data_url = f"https://www.duelingbook.com/view-replay?id={replay_id}"
        form_data = {"token": g_response, "recaptcha_version": 3, "master": False}
        response = client.post(url=data_url, data=form_data)

        replay_data = response.json()

    if not isinstance(replay_data, dict):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from DuelingBook",
        )

    if "plays" not in replay_data:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from DuelingBook",
        )

    return replay_data
