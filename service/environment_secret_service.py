import os

from core.interfaces.abstract_secret_service import AbstractSecretService


class EnvironmentSecretService(AbstractSecretService):
    def __init__(self):
        super().__init__()

    def get_api_key(self, identifier: str) -> str:
        return os.environ.get(identifier + "_API_KEY")

    def get_secret(self, identifier: str) -> str:
        return os.environ.get(identifier + "_API_SECRET")
