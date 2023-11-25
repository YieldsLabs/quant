from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class BOPFlipSignal(Signal):
    type: SignalType = SignalType.BopFlip
    smoothing_period: Parameter = StaticParameter(14.0)
