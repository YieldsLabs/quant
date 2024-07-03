from dataclasses import dataclass

from core.models.parameter import CategoricalParameter, Parameter, StaticParameter
from core.models.smooth import SmoothATR
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class Vi2LinesCrossSignal(Signal):
    type: SignalType = SignalType.Vi2LinesCross
    period: Parameter = StaticParameter(8.0)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(1.0)
