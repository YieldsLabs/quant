from dataclasses import dataclass

from core.models.candle import CandleTrendType
from core.models.parameter import CategoricalParameter, Parameter
from strategy.generator.signal.base import Signal, SignalType


@dataclass(frozen=True)
class CandlestickTrendSignal(Signal):
    type: SignalType = SignalType.CandlestickTrend
    candle: Parameter = CategoricalParameter(CandleTrendType)
