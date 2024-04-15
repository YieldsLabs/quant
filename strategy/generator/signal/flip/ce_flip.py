from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CeFlipSignal(Signal):
    type: SignalType = SignalType.CeFlip
    period: Parameter = StaticParameter(22.0)
    atr_period: Parameter = StaticParameter(22.0)
    factor: Parameter = StaticParameter(3.0)
