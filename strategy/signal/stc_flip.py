from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class STCFlipSignal(BaseSignal):
    type: SignalType = SignalType.StcFlip
    fast_period: Parameter = StaticParameter(26.0)
    slow_period: Parameter = StaticParameter(50.0)
    period: Parameter = StaticParameter(12.0)
    factor: Parameter = StaticParameter(0.5)
