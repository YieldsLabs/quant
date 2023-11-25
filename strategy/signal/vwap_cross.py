from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class VWAPCrossSignal(Signal):
    type: SignalType = SignalType.VwapCross
    period: Parameter = StaticParameter(100.0)
