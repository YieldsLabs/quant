from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.candle import TrendCandleType


@dataclass(frozen=True)
class TrendCandleSignal(Indicator):
    candle: TrendCandleType = TrendCandleType.THREE_CANDLES

    @property
    def parameters(self):
        return [
            self.candle
        ]