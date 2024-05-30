from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class VolumeAnalysis:
    obv: List[float]
    vo: List[float]
    nvol: List[float]

    def __str__(self) -> str:
        return f"obv={self.obv}, vo={self.vo}, nvol={self.nvol}"

    def __repr__(self) -> str:
        return f"VolumeAnalysis({self})"


@dataclass(frozen=True)
class VolatilityAnalysis:
    tr: List[float]

    def __str__(self) -> str:
        return f"tr={self.tr}"

    def __repr__(self) -> str:
        return f"VolatilityAnalysis({self})"


@dataclass(frozen=True)
class TrendAnalysis:
    fma: List[float]
    sma: List[float]
    macd: List[float]
    ppo: List[float]
    hh: List[float]
    ll: List[float]

    def __str__(self) -> str:
        return f"fma={self.fma}, sma={self.sma}, macd={self.macd}, ppo={self.ppo}, hh={self.hh}, ll={self.ll}"

    def __repr__(self) -> str:
        return f"TrendAnalysis({self})"


@dataclass(frozen=True)
class MomentumAnalysis:
    froc: List[float]
    sroc: List[float]
    cci: List[float]

    def __str__(self) -> str:
        return f"froc={self.froc}, sroc={self.sroc}, cci={self.cci}"

    def __repr__(self) -> str:
        return f"MomentumAnalysis({self})"


@dataclass(frozen=True)
class OscillatorAnalysis:
    frsi: List[float]
    srsi: List[float]
    bbp: List[float]
    k: List[float]
    d: List[float]

    def __str__(self) -> str:
        return f"frsi={self.frsi}, srsi={self.srsi}, bbp={self.bbp}, k={self.k}, d={self.d}"

    def __repr__(self) -> str:
        return f"OscillatorAnalysis({self})"


@dataclass(frozen=True)
class TechAnalysis:
    trend: TrendAnalysis
    momentum: MomentumAnalysis
    oscillator: OscillatorAnalysis
    volume: VolumeAnalysis
    volatility: VolatilityAnalysis

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
            ppo,
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

        trend = TrendAnalysis(fma, sma, macd, ppo, hh, ll)
        momentum = MomentumAnalysis(froc, sroc, cci)
        oscillator = OscillatorAnalysis(frsi, srsi, bbp, k, d)
        volume = VolumeAnalysis(obv, vo, nvol)
        volatility = VolatilityAnalysis(tr)

        return cls(trend, momentum, oscillator, volume, volatility)

    def __str__(self) -> str:
        return (
            f"trend={self.trend}, momentum={self.momentum}, oscillator={self.oscillator}, "
            f"volume={self.volume}, volatility={self.volatility}"
        )

    def __repr__(self) -> str:
        return f"TechAnalysis({self})"
