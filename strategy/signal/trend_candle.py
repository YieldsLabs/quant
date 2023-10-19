from dataclasses import dataclass

from core.models.candle import TrendCandleType
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class TrendCandleSignal(BaseSignal):
    type: SignalType = SignalType.TrendCandle
    candle: TrendCandleType = TrendCandleType.THREE_CANDLES
