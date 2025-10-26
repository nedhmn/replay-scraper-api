from anticaptchaofficial.recaptchav3proxyless import recaptchaV3Proxyless  # type: ignore

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
        raise ValueError("Error with the CAPTCHA")

    return g_response
