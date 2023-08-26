from dataclasses import dataclass, field
from typing import Any, List

from .base import Command

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


@dataclass(frozen=True)
class PositionRiskActorStart(Command):
    position: Position


@dataclass(frozen=True)
class SignalActorStop(Command):
    symbol: Symbol
    timeframe: Timeframe


@dataclass(frozen=True)
class PositionRiskActorStop(Command):
    position: Position