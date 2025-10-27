import base64

import bcrypt
from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_api_key_hash(plain_key: str, key_hash: str) -> bool:
    return bcrypt.checkpw(plain_key.encode(), base64.b64decode(key_hash))


async def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")) -> None:
    # Bypass auth in local environment for testing
    if settings.ENVIRONMENT == "local":
        return

    if not verify_api_key_hash(x_api_key, settings.API_KEY_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "x-api-key"},
        )
