from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class RSIVSignal(BaseSignal):
    type: SignalType = SignalType.RsiV
    rsi_type: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(8.0)
    lower_barrier: Parameter = StaticParameter(20.0)
    upper_barrier: Parameter = StaticParameter(80.0)
