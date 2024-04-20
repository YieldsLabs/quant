from dataclasses import dataclass
from enum import Enum

from core.models.indicator import Indicator


class SignalType(Enum):
    # ZeroCross
    AoZeroCross = "AoZeroCross"
    ApoZeroCross = "ApoZeroCross"
    BopZeroCross = "BopZeroCross"
    CcZeroCross = "CcZeroCross"
    CfoZeroCross = "CfoZeroCross"
    DiZeroCross = "DiZeroCross"
    MacdZeroCross = "MacdZeroCross"
    QstickZeroCross = "QstickZeroCross"
    RocZeroCross = "RocZeroCross"
    TrixZeroCross = "TrixZeroCross"
    TsiZeroCross = "TsiZeroCross"
    # Signal Line
    DiSignalLine = "DiSignalLine"
    DsoSignalLine = "DsoSignalLine"
    MacdSignalLine = "MacdSignalLine"
    RsiSignalLine = "RsiSignalLine"
    StochSignalLine = "StochSignalLine"
    QstickSignalLine = "QstickSignalLine"
    TrixSignalLine = "TrixSignalLine"
    TsiSignalLine = "TsiSignalLine"
    KstSignalLine = "KstSignalLine"
    # BB
    MacdBb = "MacdBb"
    VwapBb = "VwapBb"
    # Pattern
    AoSaucer = "AoSaucer"
    HighLow = "HighLow"
    MacdColorSwitch = "MacdColorSwitch"
    RsiV = "RsiV"
    TiiV = "TiiV"
    CandlestickTrend = "CandlestickTrend"
    # Flip
    CeFlip = "CeFlip"
    SupFlip = "SupFlip"
    # Reversal
    DmiReversal = "DmiReversal"
    SnatrReversal = "SnatrReversal"
    ViReversal = "ViReversal"
    # Ma
    Ma3Cross = "Ma3Cross"
    MaTestingGround = "MaTestingGround"
    MaQuadruple = "MaQuadruple"
    MaSurpass = "MaSurpass"
    MaCross = "MaCross"
    Ma2Rsi = "Ma2Rsi"
    VwapCross = "VwapCross"
    # Neutrality
    DsoNeutralityCross = "DsoNeutralityCross"
    RsiNeutralityCross = "RsiNeutralityCross"
    RsiNeutralityPullback = "RsiNeutralityPullback"
    RsiNeutralityRejection = "RsiNeutralityRejection"
    TiiNeutralityCross = "TiiNeutralityCross"
    # Breakout
    DchMa2Breakout = "DchMa2Breakout"

    def __str__(self):
        return self.value.upper()


@dataclass(frozen=True)
class Signal(Indicator):
    type: SignalType
