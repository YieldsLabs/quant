from abc import ABC, abstractmethod

from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractMarketRepository(ABC):
    @abstractmethod
    def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass

    @abstractmethod
    def find_next_bar(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass
