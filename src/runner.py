import json
import glob
import os
from .api import call_api, display_response_info
from .config import APIConfig


def run_normal_mode(config: APIConfig, token: str) -> None:
    """Exécute une requête unique en mode normal."""
    response = call_api(config, token)
    display_response_info(response, config=config)


def run_runner_mode(config: APIConfig, token: str) -> None:
    """Exécute plusieurs requêtes en mode runner."""
    if not config.runner_dir or not os.path.isdir(config.runner_dir):
        raise ValueError(f"Le répertoire {config.runner_dir} n'existe pas")

    json_files = glob.glob(os.path.join(config.runner_dir, "*.json"))
    if not json_files:
        raise ValueError(f"Aucun fichier JSON trouvé dans {config.runner_dir}")

    for i, json_file in enumerate(sorted(json_files), 1):
        with open(json_file, "r") as f:
            body = json.load(f)

        response = call_api(config, token, body)
        display_response_info(response, body=body, file_name=os.path.basename(json_file), request_num=i, config=config)
