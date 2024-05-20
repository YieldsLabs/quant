from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class TechAnalysis:
    rsi2: List[float]
    rsi14: List[float]
    macd: List[float]
    vo: List[float]
    nvol: List[float]
    atr: List[float]
    bbp: List[float]

    @classmethod
    def from_list(cls, data: List[Any]) -> "TechAnalysis":
        rsi2, rsi14, macd, vo, nvol, atr, bbp = data

        return cls(rsi2, rsi14, macd, vo, nvol, atr, bbp)

    def __str__(self) -> str:
        return f"rsi_fast={self.rsi2}, rsi_slow={self.rsi14}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}"

    def __repr__(self) -> str:
        return f"TechAnalysis(rsi_fast={self.rsi2}, rsi_slow={self.rsi14}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp})"
