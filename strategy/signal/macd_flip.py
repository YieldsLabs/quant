from dataclasses import dataclass

from core.models.macd import MACDType
from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class MACDFlipSignal(BaseSignal):
    type: SignalType = SignalType.MacdFlip
    macd_type: Parameter = CategoricalParameter(MACDType)
    fast_period: Parameter = RandomParameter(2.0, 15.0, 1.0)
    slow_period: Parameter = RandomParameter(9.0, 26.0, 1.0)
    signal_smoothing: Parameter = StaticParameter(9.0)