from abc import abstractmethod
from typing import List, Tuple

from ..models.symbol import Symbol
from ..interfaces.abstract_event_manager import AbstractEventManager
from ..models.timeframe import Timeframe


class AbstractWS(AbstractEventManager):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def subscribe(self, timeframes_symbols: List[Tuple[Symbol, Timeframe]]):
        pass
