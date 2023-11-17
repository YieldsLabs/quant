from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class AOSaucerSignal(BaseSignal):
    type: SignalType = SignalType.AoSaucer
    short_period: Parameter = StaticParameter(5.0)
    long_period: Parameter = StaticParameter(34.0)
