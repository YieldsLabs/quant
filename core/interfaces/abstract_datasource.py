from abc import ABC, abstractmethod


class AbstractDataSource(ABC):
    @abstractmethod
    def fetch(self):
        pass
