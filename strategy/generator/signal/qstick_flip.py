from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    RandomParameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class QstickFlipSignal(Signal):
    type: SignalType = SignalType.QstickFlip
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    period: Parameter = RandomParameter(10.0, 15.0, 1.0)
