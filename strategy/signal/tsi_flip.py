from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TsiFlipSignal(Signal):
    type: SignalType = SignalType.TsiFlip
    long_period: Parameter = StaticParameter(25.0)
    short_period: Parameter = StaticParameter(13.0)
