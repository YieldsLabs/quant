from dataclasses import dataclass, field
from typing import Any, List

from .base import Command

from ..events.base import EventMeta
from ..models.symbol import Symbol
from ..models.timeframe import Timeframe
from ..models.position import Position


@dataclass(frozen=True)
class SignalActorStart(Command):
    symbol: Symbol
    timeframe: Timeframe
    wasm_path: str
    strategy_name: str
    strategy_parameters: List[Any]
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2), init=False)


@dataclass(frozen=True)
class PositionRiskActorStart(Command):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3), init=False)


@dataclass(frozen=True)
class SignalActorStop(Command):
    symbol: Symbol
    timeframe: Timeframe
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=2), init=False)


@dataclass(frozen=True)
class PositionRiskActorStop(Command):
    position: Position
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=3), init=False)