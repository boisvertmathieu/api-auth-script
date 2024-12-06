from dataclasses import dataclass
from typing import Optional, List

GATEWAY_URL = "http://127.0.0.1:5000"
GIT_PREFIX = "C:/Program Files/Git"  # TODO : Supporter le prefix Git dans AppData


@dataclass
class APIConfig:
    """Configuration de l'API et des paramètres d'authentification et d'appel."""

    client_id: str
    client_secret: str
    username: str
    password: str
    smsession: str
    grant_type: str
    base_path: str
    endpoint: str
    method: str
    headers: Optional[List[str]]
    body: Optional[str]
    runner_mode: bool = False
    runner_dir: Optional[str] = None

    def __post_init__(self):
        self.base_path = self._clean_path(self.base_path)
        self.endpoint = self._clean_path(self.endpoint) if self.endpoint else ""
        if self.runner_dir:
            self.runner_dir = self._clean_path(self.runner_dir)

    def _clean_path(self, path: str) -> str:
        return path.replace(GIT_PREFIX, "")
