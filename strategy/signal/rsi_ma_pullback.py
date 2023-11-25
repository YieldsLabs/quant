from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
)
from core.models.rsi import RSIType
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class RSIMovingAveragePullbackSignal(Signal):
    type: SignalType = SignalType.RsiMaPullback
    rsi_type: Parameter = CategoricalParameter(RSIType)
    rsi_period: Parameter = RandomParameter(12.0, 15.0, 1.0)
    smoothing_period: Parameter = RandomParameter(7.0, 10.0, 1.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
