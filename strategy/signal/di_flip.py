from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class DIFlipSignal(BaseSignal):
    type: SignalType = SignalType.DiFlip
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
