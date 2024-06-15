from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class Vi2LinesCrossSignal(Signal):
    type: SignalType = SignalType.Vi2LinesCross
    period: Parameter = StaticParameter(14.0)
    smooth_atr: Parameter = StaticParameter(Smooth)
    period_atr: Parameter = StaticParameter(1.0)
