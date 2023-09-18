from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.trend_candle import TrendCandleType


@dataclass(frozen=True)
class CandleMAIndicator(Indicator):
    type: TrendCandleType = TrendCandleType.THREE_CANDLES

    @property
    def parameters(self):
        return []