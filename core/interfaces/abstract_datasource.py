from abc import ABC, abstractmethod

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: Symbol, timeframe: Timeframe, lookback: int):
        pass