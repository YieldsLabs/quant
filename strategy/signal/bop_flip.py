from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class BOPFlipSignal(BaseSignal):
    type: SignalType = SignalType.BopFlip
    smoothing_period: Parameter = StaticParameter(14.0)
