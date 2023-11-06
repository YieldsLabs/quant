from abc import ABC, abstractmethod


class AbstractWasmService(ABC):
    @abstractmethod
    def get_path(self, identifier: str) -> str:
        pass
