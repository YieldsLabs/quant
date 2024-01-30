from dataclasses import dataclass

from core.models.macd import MACDType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class MacdFlipSignal(Signal):
    type: SignalType = SignalType.MacdFlip
    fast_period: Parameter = StaticParameter(12.0)
    slow_period: Parameter = StaticParameter(26.0)
    signal_period: Parameter = StaticParameter(9.0)
