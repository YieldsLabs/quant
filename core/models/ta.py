from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class TechAnalysis:
    rsifast: List[float]
    rsislow: List[float]
    mafast: List[float]
    maslow: List[float]
    macd: List[float]
    vo: List[float]
    nvol: List[float]
    tr: List[float]
    bbp: List[float]
    k: List[float]
    d: List[float]
    hh: List[float]
    ll: List[float]

    @classmethod
    def from_list(cls, data: List[Any]) -> "TechAnalysis":
        rsifast, rsislow, mafast, maslow, macd, vo, nvol, tr, bbp, k, d, hh, ll = data

        return cls(
            rsifast, rsislow, mafast, maslow, macd, vo, nvol, tr, bbp, k, d, hh, ll
        )

    def __str__(self) -> str:
        return f"rsi_fast={self.rsifast}, rsi_slow={self.rsislow}, ma_fast={self.mafast}, ma_slow={self.maslow}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll}"

    def __repr__(self) -> str:
        return f"TechAnalysis(rsi_fast={self.rsifast}, rsi_slow={self.rsislow}, ma_fast={self.mafast}, ma_slow={self.maslow}, macd_histogram={self.macd}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll})"
