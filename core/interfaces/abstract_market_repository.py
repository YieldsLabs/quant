from abc import abstractmethod

from core.interfaces.abstract_event_manager import AbstractEventManager
from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractMarketRepository(AbstractEventManager):
    @abstractmethod
    def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass

    @abstractmethod
    def find_next_bar(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass

    @abstractmethod
    def ta(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass
