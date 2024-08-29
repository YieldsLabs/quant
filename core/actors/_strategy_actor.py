from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._base_actor import BaseActor
from .policy.strategy import StrategyPolicy


class StrategyActor(BaseActor):
    _EVENTS = []

    def __init__(self, symbol: Symbol, timeframe: Timeframe):
        super().__init__()
        self._symbol = symbol
        self._timeframe = timeframe
        self._id = f"{self.symbol}_{self.timeframe}"

    @property
    def id(self) -> str:
        return self._id

    @property
    def symbol(self) -> "Symbol":
        return self._symbol

    @property
    def timeframe(self) -> "Timeframe":
        return self._timeframe

    def pre_receive(self, msg) -> bool:
        return StrategyPolicy.should_process(self, msg)
