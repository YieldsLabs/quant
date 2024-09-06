import logging
import os
from typing import Optional

from core.interfaces.abstract_secret_service import AbstractSecretService

logger = logging.getLogger(__name__)


class EnvironmentSecretService(AbstractSecretService):
    def __init__(self):
        super().__init__()

    def get_api_key(self, identifier: str) -> Optional[str]:
        return self._get_env_variable(self._format_key(identifier, "API_KEY"))

    def get_secret(self, identifier: str) -> Optional[str]:
        return self._get_env_variable(self._format_key(identifier, "API_SECRET"))

    def get_wss(self, identifier: str) -> Optional[str]:
        return self._get_env_variable(self._format_key(identifier, "WSS"))

    @staticmethod
    def _format_key(identifier: str, key_type: str) -> str:
        return f"{identifier.upper()}_{key_type}"

    @staticmethod
    def _get_env_variable(key: str) -> Optional[str]:
        value = os.environ.get(key)

        if value is None:
            logger.warning(f"Environment variable '{key}' is not set.")

        return value
