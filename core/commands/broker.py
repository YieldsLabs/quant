from dataclasses import dataclass

from .base import Command

from ..models.position import Position
from ..models.broker import MarginMode, PositionMode
from ..models.symbol import Symbol


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