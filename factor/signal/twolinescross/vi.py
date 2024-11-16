from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import SmoothATR
from factor.signal.base import Signal, SignalType


@dataclass(frozen=True)
class Vi2LinesCrossSignal(Signal):
    type: SignalType = SignalType.Vi2LinesCross
    period: Parameter = StaticParameter(6.0)
    smooth_atr: Parameter = StaticParameter(SmoothATR.UTLS)
    period_atr: Parameter = StaticParameter(1.0)
