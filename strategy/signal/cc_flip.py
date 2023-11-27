from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CcFlipSignal(Signal):
    type: SignalType = SignalType.CcFlip
    short_period: Parameter = StaticParameter(20.0)
    long_period: Parameter = StaticParameter(15.0)
    smoothing_period: Parameter = StaticParameter(13.0)
