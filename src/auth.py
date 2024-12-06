from urllib.parse import urljoin
import requests
from .config import APIConfig, GATEWAY_URL


def authenticate(config: APIConfig) -> str:
    """Authentifie l'utilisateur et retourne un access_token."""
    token_url = urljoin(GATEWAY_URL, "/api/auth")
    auth_payload = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": config.grant_type,
    }

    if config.grant_type == "password":
        if not config.username or not config.password:
            raise ValueError("Username and password are required for password grant type")
        auth_payload["username"] = config.username
        auth_payload["password"] = config.password

    response = requests.post(token_url, data=auth_payload)
    response.raise_for_status()

    token_data = response.json()
    if "access_token" not in token_data:
        raise ValueError("Authentication response does not contain 'access_token'.")
    return token_data["access_token"]
