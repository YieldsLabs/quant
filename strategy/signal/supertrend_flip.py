from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class SupertrendFlipSignal(BaseSignal):
    type: SignalType = SignalType.SupFlip
    atr_period: Parameter = StaticParameter(20.0)
    factor: Parameter = StaticParameter(3.0)
