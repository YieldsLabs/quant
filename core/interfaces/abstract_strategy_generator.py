from abc import ABC, abstractmethod

from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractStrategyGenerator(ABC):
    @abstractmethod
    def generate(self) -> list[tuple[Symbol, Timeframe, Strategy]]:
        pass

    @abstractmethod
    def generate_strategies(self) -> list[Strategy]:
        pass

    @abstractmethod
    def generate_symbols(self) -> list[Symbol]:
        pass

    @abstractmethod
    def generate_timeframes(self) -> list[Timeframe]:
        pass
