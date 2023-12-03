from dataclasses import dataclass

from core.models.broker import MarginMode, PositionMode
from core.models.position import Position
from core.models.symbol import Symbol

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
