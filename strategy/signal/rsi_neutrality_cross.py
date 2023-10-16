from dataclasses import dataclass

from core.models.parameter import Parameter, RandomParameter, StaticParameter
from core.models.rsi import RSIType
from strategy.signal.base import BaseSignal, SignalType


@dataclass(frozen=True)
class RSINautralityCrossSignal(BaseSignal):
    type: SignalType = SignalType.RsiNeutralityCross
    rsi_type: RSIType = RSIType.RSI
    rsi_period: Parameter = StaticParameter(21.0)
    threshold: Parameter = RandomParameter(3.0, 7.0, 1.0)

    @property
    def parameters(self):
        return [
            self.rsi_type,
            self.rsi_period,
            self.threshold,
        ]
