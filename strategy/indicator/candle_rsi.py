from dataclasses import dataclass

from core.models.indicator import Indicator
from core.models.parameter import StaticParameter
from core.models.candle import TrendCandleType


@dataclass(frozen=True)
class CandleRSIIndicator(Indicator):
    type: TrendCandleType = TrendCandleType.DOUBLE_TROUBLE
    rsi_period = StaticParameter(14)

    @property
    def parameters(self):
        return [int(self.rsi_period.value)]