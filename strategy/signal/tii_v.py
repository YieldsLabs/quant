from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TIIVSignal(BaseSignal):
    type: SignalType = SignalType.TiiV
    major_period: Parameter = StaticParameter(5.0)
    minor_period: Parameter = StaticParameter(2.0)
