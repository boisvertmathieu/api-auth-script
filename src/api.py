from urllib.parse import urljoin
import requests
import json
from typing import Optional, Dict
from .config import APIConfig, GATEWAY_URL


def build_uri(base_path: str, endpoint: str) -> str:
    """Construit l'URL complète à partir du base_path et de l'endpoint."""
    api_index = base_path.find("/api")
    clean_path = base_path[api_index:] if api_index != -1 else base_path

    url = urljoin(GATEWAY_URL, clean_path)
    if endpoint:
        if not url.endswith("/"):
            url += "/"
        url = urljoin(url, endpoint.lstrip("/"))

    return url


def parse_headers(header_list: list) -> dict:
    """Transforme une liste de headers au format 'clé=valeur' en dictionnaire."""
    headers = {}
    if not header_list:
        return headers
    for h in header_list:
        if "=" in h:
            k, v = h.split("=", 1)
            headers[k.strip()] = v.strip()
    return headers


def call_api(config: APIConfig, token: str, body: Optional[Dict] = None) -> requests.Response:
    """Appelle l'API avec la configuration donnée."""
    url = build_uri(config.base_path, config.endpoint)
    user_headers = parse_headers(config.headers)
    user_headers["Authorization"] = f"Bearer {token}"
    user_headers.setdefault("Content-Type", "application/json")

    data = json.dumps(body) if isinstance(body, dict) else config.body
    response = requests.request(config.method, url, headers=user_headers, data=data)
    return response


def display_response_info(
    response: requests.Response,
    body: Optional[Dict] = None,
    file_name: Optional[str] = None,
    request_num: Optional[int] = None,
    config: Optional[APIConfig] = None,
) -> None:
    """Affiche les informations de la requête et de la réponse."""
    print("=" * 80)
    if file_name:
        print(f"Fichier: {file_name}")
    if request_num is not None:
        print(f"Requête #{request_num}")
    if config:
        print(f"URL: {build_uri(config.base_path, config.endpoint)}")
        print(f"Méthode: {config.method}")
    if body:
        print(f"Body envoyé: {json.dumps(body, indent=2)}")
    print(f"Status: {response.status_code}")
    print(f"Réponse: {json.dumps(response.json(), indent=2)}")
    print("=" * 80)
