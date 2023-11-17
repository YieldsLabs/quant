from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class DMICrossSignal(BaseSignal):
    type: SignalType = SignalType.DmiCross
    adx_period: Parameter = StaticParameter(12.0)
    di_period: Parameter = StaticParameter(12.0)
