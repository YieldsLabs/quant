from abc import ABC, abstractmethod


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: str, timeseries: str):
        raise NotImplementedError
