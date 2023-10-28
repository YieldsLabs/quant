from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class SignalType(Enum):
    AoFlip = "AoFlip"
    Ma3Cross = "Ma3Cross"
    MacdFlip = "MacdFlip"
    MacdCross = "MacdCross"
    MacdColorSwitch = "MacdColorSwitch"
    RsiNeutralityCross = "RsiNeutralityCross"
    RsiNeutralityPullback = "RsiNeutralityPullback"
    RsiNeutralityRejection = "RsiNeutralityRejection"
    Rsi2Ma = "Rsi2Ma"
    Dch2Ma = "Dch2Ma"
    RocFlip = "RocFlip"
    RsiV = "RsiV"
    SnAtr = "SnAtr"
    SupFlip = "SupFlip"
    SupPullBack = "SupPullBack"
    TestGround = "TestGround"
    TrendCandle = "TrendCandle"
    TIICross = "TIICross"
    TiiV = "TiiV"
    TrixFlip = "TrixFlip"
    TsiFlip = "TsiFlip"
    TsiCross = "TsiCross"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseSignal(Indicator):
    type: SignalType
