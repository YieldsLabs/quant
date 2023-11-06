from abc import ABC, abstractmethod

from core.models.lookback import Lookback
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractDataSource(ABC):
    @abstractmethod
    def fetch(
        self, symbol: Symbol, timeframe: Timeframe, lookback: Lookback, batch_size: int
    ):
        pass
