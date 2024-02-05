from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    RandomParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class RsiMaPullbackSignal(Signal):
    type: SignalType = SignalType.RsiMaPullback
    rsi_period: Parameter = RandomParameter(12.0, 15.0, 1.0)
    smooth_type: Parameter = CategoricalParameter(Smooth)
    smoothing_period: Parameter = RandomParameter(7.0, 10.0, 1.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
