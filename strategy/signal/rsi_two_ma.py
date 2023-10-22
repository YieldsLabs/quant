from dataclasses import dataclass
from inspect import Parameter

from core.models.moving_average import MovingAverageType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class RSI2MovingAverageSignal(BaseSignal):
    type: SignalType = SignalType.Rsi2Ma
    rsi_type: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(2.0)
    lower_barrier: Parameter = StaticParameter(20.0)
    upper_barrier: Parameter = StaticParameter(80.0)
    smoothing: MovingAverageType = MovingAverageType.EMA
    short_period: Parameter = RandomParameter(20.0, 50.0, 5.0)
    long_period: Parameter = RandomParameter(30.0, 50.0, 5.0)
