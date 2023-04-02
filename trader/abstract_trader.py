from abc import ABC, abstractmethod
from typing import Type

from strategy.abstract_strategy import AbstractStrategy

class AbstractTrader(ABC):
    @abstractmethod
    def trade(self, strategy: Type[AbstractStrategy], symbol: str, timeframe: str) -> None:
        pass