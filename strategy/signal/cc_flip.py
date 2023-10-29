from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class CCFlipSignal(BaseSignal):
    type: SignalType = SignalType.CcFlip
    short_period: Parameter = StaticParameter(11.0)
    long_period: Parameter = StaticParameter(14.0)
    smoothing_period: Parameter = StaticParameter(10.0)
