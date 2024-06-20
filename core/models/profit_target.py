from dataclasses import dataclass
from functools import cached_property

import numpy as np

from core.models.side import SignalSide


@dataclass(frozen=True)
class ProfitTarget:
    side: SignalSide
    entry: float
    volatility: float

    @cached_property
    def context_factor(self):
        return 1.0 if self.side == SignalSide.BUY else -1.0

    @cached_property
    def first(self):
        return self._pt(0.3, 0.6)

    @cached_property
    def second(self):
        return self._pt(0.8, 1.5)

    @cached_property
    def third(self):
        return self._pt(1.6, 2.5)

    @cached_property
    def fourth(self):
        return self._pt(2.6, 3.8)

    @cached_property
    def fifth(self):
        return self._pt(3.9, 4.8)

    @cached_property
    def last(self):
        return self.fifth

    def _pt(self, min_scale: float, max_scale: float) -> float:
        scale = np.random.uniform(min_scale, max_scale)
        target_price = self.entry * (1 + self.volatility * self.context_factor * scale)

        if self.context_factor == 1:
            return max(target_price, self.entry)
        else:
            return min(target_price, self.entry)

    def to_dict(self):
        return {
            "first": self.first,
            "second": self.second,
            "third": self.third,
            "fourth": self.fourth,
            "fifth": self.fifth,
        }
