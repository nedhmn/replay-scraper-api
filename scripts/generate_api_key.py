import base64
import secrets

import bcrypt


def generate_api_key() -> tuple[str, str]:
    api_key = f"api_{secrets.token_urlsafe(32)}"
    key_hash = bcrypt.hashpw(api_key.encode(), bcrypt.gensalt())

    return api_key, base64.b64encode(key_hash).decode()


if __name__ == "__main__":
    plain_key, hashed_key = generate_api_key()

    print("\nPlain API Key (distribute to clients):")
    print(f"  API_KEY={plain_key}")
    print(f"  API_KEY_HASH={hashed_key}")
