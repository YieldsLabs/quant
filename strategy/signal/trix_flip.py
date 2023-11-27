from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class TrixFlipSignal(Signal):
    type: SignalType = SignalType.TrixFlip
    period: Parameter = StaticParameter(18.0)
