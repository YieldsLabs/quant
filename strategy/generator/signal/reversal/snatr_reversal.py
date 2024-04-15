from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.smooth import Smooth
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SnatrReversalSignal(Signal):
    type: SignalType = SignalType.SnatrReversal
    smooth_type: Parameter = StaticParameter(Smooth.WMA)
    atr_period: Parameter = StaticParameter(60.0)
    atr_smooth_period: Parameter = StaticParameter(13.0)
    threshold: Parameter = RandomParameter(0.0, 0.2, 0.1)
