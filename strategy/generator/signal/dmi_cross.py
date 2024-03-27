from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth

from .base import Signal, SignalType


@dataclass(frozen=True)
class DmiCrossSignal(Signal):
    type: SignalType = SignalType.DmiCross
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    adx_period: Parameter = StaticParameter(4.0)
    di_period: Parameter = StaticParameter(4.0)
