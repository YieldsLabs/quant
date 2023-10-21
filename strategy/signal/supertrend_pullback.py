from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class SupertrendPullBackSignal(BaseSignal):
    type: SignalType = SignalType.SupPullBack
    atr_period: Parameter = RandomParameter(15.0, 25.0, 5.0)
    factor: Parameter = RandomParameter(2.0, 5.0, 1.0)
