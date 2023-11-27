from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CfoFlipSignal(Signal):
    type: SignalType = SignalType.CfoFlip
    period: Parameter = StaticParameter(14.0)
