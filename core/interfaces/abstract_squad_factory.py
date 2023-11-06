from abc import ABC, abstractmethod

from core.interfaces.abstract_squad import AbstractSquad
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractSquadFactory(ABC):
    @abstractmethod
    def create_squad(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
    ) -> AbstractSquad:
        pass
