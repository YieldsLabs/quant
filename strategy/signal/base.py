from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class SignalType(Enum):
    AoFlip = "AoFlip"
    AoSaucer = "AoSaucer"
    CcFlip = "CcFlip"
    DiFlip = "DiFlip"
    DiCross = "DiCross"
    DmiCross = "DmiCross"
    Ma3Cross = "Ma3Cross"
    MacdFlip = "MacdFlip"
    MacdCross = "MacdCross"
    MacdColorSwitch = "MacdColorSwitch"
    RsiNeutralityCross = "RsiNeutralityCross"
    RsiNeutralityPullback = "RsiNeutralityPullback"
    RsiNeutralityRejection = "RsiNeutralityRejection"
    Rsi2Ma = "Rsi2Ma"
    RsiMaPullback = "RsiMaPullback"
    Dch2Ma = "Dch2Ma"
    RocFlip = "RocFlip"
    RsiV = "RsiV"
    SnAtr = "SnAtr"
    SupFlip = "SupFlip"
    SupPullBack = "SupPullBack"
    StcFlip = "StcFlip"
    StcUturn = "StcUturn"
    StochCross = "StochCross"
    TestGround = "TestGround"
    TrendCandle = "TrendCandle"
    TIICross = "TIICross"
    TiiV = "TiiV"
    TrixFlip = "TrixFlip"
    TsiFlip = "TsiFlip"
    TsiCross = "TsiCross"
    QstickFlip = "QstickFlip"
    QstickCross = "QstickCross"
    Quadruple = "Quadruple"
    VwapCross = "VwapCross"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class BaseSignal(Indicator):
    type: SignalType
