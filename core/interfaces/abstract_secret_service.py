from abc import ABC, abstractmethod


class AbstractSecretService(ABC):
    @abstractmethod
    def get_api_key(self, identifier: str) -> str:
        pass

    @abstractmethod
    def get_secret(self, identifier: str) -> str:
        pass
