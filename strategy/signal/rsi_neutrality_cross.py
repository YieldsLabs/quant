from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class RSINautralityCrossSignal(BaseSignal):
    type: SignalType = SignalType.RsiNeutralityCross
    rsi_type: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(21.0)
    threshold: Parameter = StaticParameter(0.0)
