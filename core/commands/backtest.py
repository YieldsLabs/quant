from dataclasses import dataclass

from .base import Command

from ..models.symbol import Symbol
from ..interfaces.abstract_datasource import AbstractDatasource
from ..models.lookback import TIMEFRAMES_TO_LOOKBACK, Lookback


@dataclass(frozen=True)
class BacktestRun(Command):
    datasource: AbstractDatasource
    symbol: Symbol
    timeframe: TIMEFRAMES_TO_LOOKBACK
    lookback: Lookback
    batch_size: int
