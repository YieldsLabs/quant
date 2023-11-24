from dataclasses import dataclass

from core.models.parameter import (
    Parameter,
    StaticParameter,
)
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TRIXCrossSignal(BaseSignal):
    type: SignalType = SignalType.TrixCross
    period: Parameter = StaticParameter(18.0)
    signal_period: Parameter = StaticParameter(9.0)
