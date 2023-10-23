from dataclasses import dataclass

from core.models.candle import TrendCandleType
from core.models.parameter import CategoricalParameter, Parameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TrendCandleSignal(BaseSignal):
    type: SignalType = SignalType.TrendCandle
    candle: Parameter = CategoricalParameter(TrendCandleType)
