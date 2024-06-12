from dataclasses import dataclass
from functools import cached_property

import numpy as np

from core.models.side import SignalSide
from core.models.signal import Signal


@dataclass(frozen=True)
class ProfitTarget:
    signal: Signal
    volatility: float

    @cached_property
    def context_factor(self):
        return 1.0 if self.signal.side == SignalSide.BUY else -1.0

    @cached_property
    def first(self):
        scale = np.random.uniform(0.3, 0.6)
        return self._pt(scale)

    @cached_property
    def second(self):
        scale = np.random.uniform(0.8, 1.5)
        return self._pt(scale)

    @cached_property
    def last(self):
        return self.second

    def _pt(self, scale: float) -> float:
        return self.signal.ohlcv.close * (
            1 + self.volatility * self.context_factor * scale
        )

    def to_dict(self):
        return {
            "ft": self.first,
            "st": self.second,
        }
