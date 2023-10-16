from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple

from core.models.indicator import Indicator


class SignalType(Enum):
    Ma3Cross = "Ma3Cross"
    RsiNeutralityCross = "RsiNeutralityCross"
    Rsi2Ma = "Rsi2Ma"
    RsiV = "RsiV"
    SnAtr = "SnAtr"
    SupFlip = "SupFlip"
    Testground = "Testground"
    Trendcandle = "Trendcandle"
    TIICross = "TIICross"


@dataclass(frozen=True)
class BaseSignal(Indicator):
    type: SignalType

    def parameters(self) -> Tuple[Any, ...]:
        return []
