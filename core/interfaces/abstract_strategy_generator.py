from abc import ABC, abstractmethod

from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractStrategyGenerator(ABC):
    @abstractmethod
    def generate(
        self, symbols: list[Symbol], timeframes: list[Timeframe]
    ) -> list[tuple[Symbol, Timeframe, Strategy]]:
        pass
