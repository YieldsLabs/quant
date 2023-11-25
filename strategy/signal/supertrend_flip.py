from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import Signal, SignalType


@dataclass(frozen=True)
class SupertrendFlipSignal(Signal):
    type: SignalType = SignalType.SupFlip
    atr_period: Parameter = StaticParameter(10.0)
    factor: Parameter = StaticParameter(3.0)
