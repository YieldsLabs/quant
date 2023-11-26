from dataclasses import dataclass

from core.interfaces.abstract_datasource import AbstractDataSource
from core.models.lookback import Lookback
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Command


@dataclass(frozen=True)
class BacktestRun(Command):
    datasource: AbstractDataSource
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    in_sample: Lookback
    out_sample: Lookback | None
