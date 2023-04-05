from abc import ABC, abstractmethod

from shared.timeframes import Timeframes


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: str, timeframe: Timeframes):
        raise NotImplementedError
