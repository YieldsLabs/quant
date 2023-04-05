from abc import ABC, abstractmethod
from typing import Type
from ohlcv.context import ohlcv
from shared.timeframes import Timeframes

from strategy.abstract_strategy import AbstractStrategy


@ohlcv
class AbstractTrader(ABC):
    @abstractmethod
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: Timeframes) -> None:
        raise NotImplementedError
