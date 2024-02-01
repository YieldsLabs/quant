from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)

from .base import Signal, SignalType


@dataclass(frozen=True)
class RsiSupertrendSignal(Signal):
    type: SignalType = SignalType.RsiSup
    rsi_period: Parameter = StaticParameter(34.0)
    threshold: Parameter = RandomParameter(2.0, 4.0, 1.0)
    atr_period: Parameter = StaticParameter(10.0)
    factor: Parameter = StaticParameter(3.0)
