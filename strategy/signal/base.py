from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class SignalType(Enum):
    Ma3Cross = "Ma3Cross"
    RsiNeutralityCross = "RsiNeutralityCross"
    Rsi2Ma = "Rsi2Ma"
    RsiV = "RsiV"
    SnAtr = "SnAtr"
    SupFlip = "SupFlip"
    TestGround = "TestGround"
    TrendCandle = "TrendCandle"
    TIICross = "TIICross"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseSignal(Indicator):
    type: SignalType
