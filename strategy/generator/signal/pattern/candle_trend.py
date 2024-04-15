from dataclasses import dataclass

from core.models.candle import CandleTrendType
from core.models.parameter import CategoricalParameter, Parameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CandleTrendSignal(Signal):
    type: SignalType = SignalType.CandleTrend
    candle: Parameter = CategoricalParameter(CandleTrendType)
