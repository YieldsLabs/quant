from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TIICrossSignal(BaseSignal):
    type: SignalType = SignalType.TIICross
    major_period: Parameter = StaticParameter(60.0)
    minor_period: Parameter = StaticParameter(30.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
