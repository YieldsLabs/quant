from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class Dmi2LinesCrossSignal(Signal):
    type: SignalType = SignalType.Dmi2LinesCross
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    adx_period: Parameter = StaticParameter(8.0)
    di_period: Parameter = StaticParameter(8.0)
