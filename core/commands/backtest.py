from dataclasses import dataclass

from core.models.datasource import DataSourceType
from core.models.exchange import ExchangeType
from core.models.lookback import Lookback
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Command


@dataclass(frozen=True)
class BacktestRun(Command):
    datasource: DataSourceType
    exchange: ExchangeType
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
    in_sample: Lookback
    out_sample: Lookback | None
