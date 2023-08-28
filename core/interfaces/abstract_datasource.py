from abc import ABC, abstractmethod

from ..models.timeframe import Timeframe


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: str, timeframe: Timeframe, lookback: int):
        pass