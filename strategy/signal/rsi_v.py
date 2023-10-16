from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import RandomParameter, StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import BaseSignal


@dataclass(frozen=True)
class RSIVSignal(BaseSignal):
    rsi_type: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(8.0)
    lower_barrier: Parameter = RandomParameter(5.0, 15.0, 5.0)
    upper_barrier: Parameter = RandomParameter(80.0, 95.0, 5.0)

    @property
    def parameters(self):
        return [
            self.rsi_type,
            self.rsi_period,
            self.lower_barrier,
            self.upper_barrier,
        ]
