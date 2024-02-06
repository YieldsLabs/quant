from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class TsiFlipSignal(Signal):
    type: SignalType = SignalType.TsiFlip
    smooth_type: Parameter = StaticParameter(Smooth.EMA)
    long_period: Parameter = StaticParameter(25.0)
    short_period: Parameter = StaticParameter(13.0)
