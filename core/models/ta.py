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
    k: List[float]
    d: List[float]
    hh: List[float]
    ll: List[float]

    @classmethod
    def from_list(cls, data: List[Any]) -> "TechAnalysis":
        rsi2, rsi14, macd, vo, nvol, atr, bbp, k, d, hh, ll = data

        return cls(rsi2, rsi14, macd, vo, nvol, atr, bbp, k, d, hh, ll)

    def __str__(self) -> str:
        return f"rsi_fast={self.rsi2}, rsi_slow={self.rsi14}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll}"

    def __repr__(self) -> str:
        return f"TechAnalysis(rsi_fast={self.rsi2}, rsi_slow={self.rsi14}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll})"
