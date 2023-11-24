from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class STCUTurnSignal(BaseSignal):
    type: SignalType = SignalType.StcUturn
    fast_period: Parameter = StaticParameter(26.0)
    slow_period: Parameter = StaticParameter(50.0)
    cycle: Parameter = StaticParameter(10.0)
    d_first: Parameter = StaticParameter(3.0)
    d_second: Parameter = StaticParameter(3.0)
