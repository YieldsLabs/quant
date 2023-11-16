from dataclasses import dataclass
from core.models.parameter import Parameter, StaticParameter

from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class VWAPCrossSignal(BaseSignal):
    type: SignalType = SignalType.VwapCross
    period: Parameter = StaticParameter(200.0)