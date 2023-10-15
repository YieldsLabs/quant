from dataclasses import dataclass

from core.models.candle import TrendCandleType
from core.models.indicator import Indicator


@dataclass(frozen=True)
class TrendCandleSignal(BaseSignal):
    candle: TrendCandleType = TrendCandleType.THREE_CANDLES

    @property
    def parameters(self):
        return [self.candle]
