from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TRIXFlipSignal(BaseSignal):
    type: SignalType = SignalType.TrixFlip
    period: Parameter = StaticParameter(18.0)
