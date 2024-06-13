from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class DmiLines2CrossSignal(Signal):
    type: SignalType = SignalType.DmiLines2Cross
    smooth_type: Parameter = StaticParameter(Smooth.SMMA)
    adx_period: Parameter = StaticParameter(8.0)
    di_period: Parameter = StaticParameter(14.0)
