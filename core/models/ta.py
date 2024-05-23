from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class TechAnalysis:
    frsi: List[float]
    srsi: List[float]
    fma: List[float]
    sma: List[float]
    froc: List[float]
    sroc: List[float]
    macd: List[float]
    cci: List[float]
    obv: List[float]
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
        (
            frsi,
            srsi,
            fma,
            sma,
            froc,
            sroc,
            macd,
            cci,
            obv,
            vo,
            nvol,
            tr,
            bbp,
            k,
            d,
            hh,
            ll,
        ) = data

        return cls(
            frsi,
            srsi,
            fma,
            sma,
            froc,
            sroc,
            macd,
            cci,
            obv,
            vo,
            nvol,
            tr,
            bbp,
            k,
            d,
            hh,
            ll,
        )

    def __str__(self) -> str:
        return f"rsi_fast={self.frsi}, rsi_slow={self.srsi}, ma_fast={self.fma}, ma_slow={self.sma}, roc_fast={self.froc}, roc_slow={self.sroc}, macd_histogram={self.macd}, cci={self.cci}, obv={self.obv}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll}"

    def __repr__(self) -> str:
        return f"TechAnalysis(rsi_fast={self.frsi}, rsi_slow={self.srsi}, ma_fast={self.fma}, ma_slow={self.sma}, roc_fast={self.froc}, roc_slow={self.sroc}, macd_histogram={self.macd}, cci={self.cci}, obv={self.obv}, volume_osc={self.vo}, volume_normalized={self.nvol}, atr={self.atr}, bb%b={self.bbp}, stoch_k={self.k}, stoch_d={self.d}, hh={self.hh}, ll={self.ll})"
