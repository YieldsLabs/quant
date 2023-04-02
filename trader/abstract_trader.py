from abc import ABC, abstractmethod
from typing import Type
from shared.ohlcv_context import inject_ohlcv

from strategy.abstract_strategy import AbstractStrategy

@inject_ohlcv
class AbstractTrader(ABC):
    @abstractmethod
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: str) -> None:
        raise NotImplementedError