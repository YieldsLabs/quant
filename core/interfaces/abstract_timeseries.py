from abc import ABC, abstractmethod
from typing import Optional

from core.models.ohlcv import OHLCV
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractTimeSeriesService(ABC):
    @abstractmethod
    async def upsert(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass

    @abstractmethod
    async def next_bar(
        self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV
    ) -> Optional[OHLCV]:
        pass

    @abstractmethod
    async def prev_bar(
        self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV
    ) -> Optional[OHLCV]:
        pass

    @abstractmethod
    async def ta(self, symbol: Symbol, timeframe: Timeframe, bar: OHLCV):
        pass
