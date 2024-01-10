from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Signal, SignalType


@dataclass(frozen=True)
class SupertrendPullBackSignal(Signal):
    type: SignalType = SignalType.SupPullBack
    atr_period: Parameter = StaticParameter(10.0)
    factor: Parameter = StaticParameter(2.0)
