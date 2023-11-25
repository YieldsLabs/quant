from dataclasses import dataclass
from inspect import Parameter

from core.models.parameter import CategoricalParameter, RandomParameter, StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class RSIVSignal(Signal):
    type: SignalType = SignalType.RsiV
    rsi_type: Parameter = CategoricalParameter(RSIType)
    rsi_period: Parameter = StaticParameter(8.0)
    threshold: Parameter = RandomParameter(0.0, 3.0, 1.0)
