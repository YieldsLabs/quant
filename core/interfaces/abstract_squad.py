from abc import ABC, abstractmethod

from ..models.strategy import Strategy
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractSquad(ABC):
    @property
    @abstractmethod
    def symbol(self) -> Symbol:
        pass

    @property
    @abstractmethod
    def timeframe(self) -> Timeframe:
        pass

    @property
    @abstractmethod
    def strategy(self) -> Strategy:
        pass
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass