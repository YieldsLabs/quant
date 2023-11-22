from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class HighLowSignal(BaseSignal):
    type: SignalType = SignalType.HighLow
    period: Parameter = StaticParameter(3.0)
