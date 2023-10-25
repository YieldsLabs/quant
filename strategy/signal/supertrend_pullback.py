from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class SupertrendPullBackSignal(BaseSignal):
    type: SignalType = SignalType.SupPullBack
    atr_period: Parameter = StaticParameter(10.0)
    factor: Parameter = StaticParameter(3.0)
