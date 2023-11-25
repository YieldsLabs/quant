from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class APOFlipSignal(Signal):
    type: SignalType = SignalType.ApoFlip
    short_period: Parameter = StaticParameter(10.0)
    long_period: Parameter = StaticParameter(20.0)
