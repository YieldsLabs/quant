from dataclasses import dataclass
from typing import List, Tuple

from core.models.broker import MarginMode, PositionMode
from core.models.position import Position
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from .base import Command


@dataclass(frozen=True)
class UpdateSettings(Command):
    symbol: Symbol
    leverage: int
    position_mode: PositionMode
    margin_mode: MarginMode


@dataclass(frozen=True)
class OpenPosition(Command):
    position: Position


@dataclass(frozen=True)
class ClosePosition(Command):
    position: Position


@dataclass(frozen=True)
class Subscribe(Command):
    symbols_and_timeframes: List[Tuple[Symbol, Timeframe]]
