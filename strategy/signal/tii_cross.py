from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TIICrossSignal(BaseSignal):
    type: SignalType = SignalType.TIICross
    major_period: Parameter = StaticParameter(60.0)
    minor_period: Parameter = StaticParameter(30.0)
    lower_barrier: Parameter = StaticParameter(40.0)
    upper_barrier: Parameter = StaticParameter(60.0)
