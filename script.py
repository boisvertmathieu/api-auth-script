import argparse
import requests
import os
import sys
from urllib.parse import urljoin
from dotenv import load_dotenv
import json

GATEWAY_URL = "http://127.0.0.1:5000"


class APIConfig:
    def __init__(
        self,
        client_id,
        client_secret,
        username,
        password,
        smsession,
        grant_type,
        base_path,
        endpoint,
        method,
        headers,
        body,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.smsession = smsession
        self.grant_type = grant_type
        self.base_path = base_path
        self.endpoint = endpoint
        self.method = method
        self.headers = headers
        self.body = body


def build_uri(base_path, endpoint):
    api_index = base_path.find("/api")
    clean_path = base_path[api_index:] if api_index != -1 else base_path

    # Construire l'URL complète
    url = urljoin(GATEWAY_URL, clean_path)
    if endpoint:
        url = urljoin(url, endpoint)

    print("URL:", url)
    return url


def authenticate(config):
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
    return response.json()["access_token"]


def call_api(config, token):
    url = build_uri(config.base_path, config.endpoint)
    headers = {header.split("=")[0]: header.split("=")[1] for header in (config.headers or [])}
    headers["Authorization"] = f"Bearer {token}"

    response = requests.request(config.method, url, headers=headers, data=config.body)
    response.raise_for_status()
    return response.json()


def main():
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Récupération des secrets depuis .env
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    smsession = os.getenv("SMSESSION")

    # Configuration de argparse
    parser = argparse.ArgumentParser(description="Script pour appeler une API en production")
    parser.add_argument(
        "--grant-type",
        help="Le type de grant_type à utiliser pour obtenir le token (e.g. 'password', 'client_credentials', etc.)",
        default="password",
    )
    parser.add_argument(
        "--base-path",
        required=True,
        help="Le path de base de l'API à appeler (ex: /api/v1)",
        type=str,
    )
    parser.add_argument(
        "--endpoint",
        default="",
        help="Un endpoint supplémentaire à ajouter après le base-path au besoin (ex: /pascal)",
        type=str,
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
        help="La méthode HTTP à utiliser",
    )
    parser.add_argument(
        "--headers",
        nargs="*",
        help='Des headers personnalisés au format key=value (ex: "X-Request-Id=1234" "Authorization=Bearer token")',
    )
    parser.add_argument(
        "--body", type=str, help='Le body de la requête (en JSON) (ex: \'{"key1": "value1", "key2": "value2"}\')'
    )

    args = parser.parse_args()

    # Création de l'objet de configuration
    config = APIConfig(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        smsession=smsession,
        grant_type=args.grant_type,
        base_path=args.base_path,
        endpoint=args.endpoint,
        method=args.method,
        headers=args.headers,
        body=args.body,
    )

    print("client_id:", config.client_id)
    print("client_secret:", config.client_secret)
    print("username:", config.username)
    print("password:", config.password)
    print("smsession:", config.smsession)
    print("grant_type:", config.grant_type)
    print("base_path:", config.base_path)
    print("endpoint:", config.endpoint)
    print("method:", config.method)
    print("headers:", config.headers)
    print("body:", config.body)

    # Authentification
    token = authenticate(config)

    # Appel à l'API
    response = call_api(config, token)
    print(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
