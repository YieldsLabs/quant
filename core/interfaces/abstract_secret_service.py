from abc import ABC, abstractmethod


class AbstractSecretService(ABC):
    @abstractmethod
    def get_api_key(self, identifier: str) -> str:
        pass

    @abstractmethod
    def get_secret(self, identifier: str) -> str:
        pass

    @abstractmethod
    def get_wss_public(self, identifier: str, type) -> str:
        pass

    @abstractmethod
    def get_wss_private(self, identifier: str) -> str:
        pass

    @abstractmethod
    def get_wss_order(self, identifier: str) -> str:
        pass
