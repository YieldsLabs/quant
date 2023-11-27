from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class AoSaucerSignal(Signal):
    type: SignalType = SignalType.AoSaucer
    short_period: Parameter = StaticParameter(5.0)
    long_period: Parameter = StaticParameter(34.0)
