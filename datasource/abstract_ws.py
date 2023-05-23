from abc import abstractmethod
from typing import List, Tuple

from core.abstract_event_manager import AbstractEventManager
from core.timeframe import Timeframe


class AbstractWS(AbstractEventManager):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def subscribe(self, timeframes_symbols: List[Tuple[str, Timeframe]]):
        pass
