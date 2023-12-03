from dataclasses import dataclass

from core.commands.base import Command
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


@dataclass(frozen=True)
class FeedRun(Command):
    symbol: Symbol
    timeframe: Timeframe
    strategy: Strategy
