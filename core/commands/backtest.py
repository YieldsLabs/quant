from dataclasses import dataclass

from core.interfaces.abstract_datasource import AbstractDatasource
from core.models.lookback import TIMEFRAMES_TO_LOOKBACK, Lookback
from core.models.symbol import Symbol

from .base import Command


@dataclass(frozen=True)
class BacktestRun(Command):
    datasource: AbstractDatasource
    symbol: Symbol
    timeframe: TIMEFRAMES_TO_LOOKBACK
    lookback: Lookback
    batch_size: int
