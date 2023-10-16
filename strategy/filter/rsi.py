from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from core.models.rsi import RSIType
from strategy.filter.base import BaseFilter


@dataclass(frozen=True)
class RSIFilter(BaseFilter):
    rsi_type: RSIType = RSIType.RSI
    period: Parameter = RandomParameter(14.0, 16.0, 1.0)
    threshold: Parameter = RandomParameter(49.0, 55.0, 1.0)

    @property
    def parameters(self):
        return [self.rsi_type, self.period, self.threshold]
