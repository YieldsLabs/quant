from abc import ABC, abstractmethod
from typing import List

from ..models.symbol import Symbol
from ..models.timeframe import Timeframe


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: str, timeframe: Timeframe, lookback: int):
        pass
    
    @abstractmethod
    def account_size(self) -> float:
        pass

    @abstractmethod
    def symbols(self) -> List[Symbol]:
        pass

    @abstractmethod
    def symbol(self, name) -> Symbol:
        pass