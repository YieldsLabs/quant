from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class RsiNautralityRejectionSignal(Signal):
    type: SignalType = SignalType.RsiNeutralityRejection
    rsi_period: Parameter = StaticParameter(14.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
