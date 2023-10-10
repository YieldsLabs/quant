from dataclasses import dataclass
from inspect import Parameter

from core.models.indicator import Indicator
from core.models.parameter import RandomParameter, StaticParameter
from core.models.rsi import RSIType


@dataclass(frozen=True)
class RSIVSignal(Indicator):
    rsi: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(8.0)
    lower_barrier: Parameter = RandomParameter(5.0, 15.0, 5.0)
    upper_barrier: Parameter = RandomParameter(80.0, 95.0, 5.0)

    @property
    def parameters(self):
        return [
            self.rsi,
            self.rsi_period,
            self.lower_barrier,
            self.upper_barrier,
        ]
