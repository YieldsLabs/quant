import logging
import os
from typing import Optional

from core.interfaces.abstract_secret_service import AbstractSecretService

logger = logging.getLogger(__name__)


class EnvironmentSecretService(AbstractSecretService):
    def __init__(self):
        super().__init__()

    def get_api_key(self, identifier: str) -> Optional[str]:
        key = f"{identifier.upper()}_API_KEY"

        return self._get_env_variable(key)

    def get_secret(self, identifier: str) -> Optional[str]:
        key = f"{identifier.upper()}_API_SECRET"

        return self._get_env_variable(key)

    def get_wss(self, identifier: str) -> Optional[str]:
        key = f"{identifier.upper()}_WSS"

        return self._get_env_variable(key)

    @staticmethod
    def _get_env_variable(key: str) -> Optional[str]:
        value = os.environ.get(key)

        if value is None:
            logger.warning(f"Environment variable '{key}' is not set.")

        return value
