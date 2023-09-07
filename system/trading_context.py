from dataclasses import dataclass
from typing import List

from core.interfaces.abstract_datasource import AbstractDatasource
from core.interfaces.abstract_squad_factory import AbstractSquadFactory
from core.models.lookback import Lookback
from core.models.timeframe import Timeframe


@dataclass
class TradingContext:
    datasource: AbstractDatasource
    squad_factory: AbstractSquadFactory
    timeframes: List[Timeframe]
    blacklist: List[str]
    lookback: Lookback
    batch_size: int
    leverage: int
    live_mode: bool
