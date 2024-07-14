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
    def targets(self):
        levels = [
            (0.236, 0.382),
            (0.618, 0.786),
            (1.0, 1.5),
            (1.786, 3.618),
            (4.0, 5.786),
            (6.0, 7.618),
            (8.0, 9.236),
            (9.618, 10.236),
            (10.618, 11.236),
            (11.618, 12.236),
            (12.618, 13.236),
            (13.618, 14.236),
        ]

        return list({self._pt(min_scale, max_scale) for min_scale, max_scale in levels})

    @cached_property
    def last(self):
        return self.targets[-1]

    def _pt(self, min_scale: float, max_scale: float) -> float:
        scale = np.random.uniform(min_scale, max_scale)
        target_price = self.entry * (1 + self.volatility * self.context_factor * scale)

        return (
            max(target_price, self.entry)
            if self.context_factor == 1
            else min(target_price, self.entry)
        )

    def to_dict(self):
        return {
            "targets": self.targets,
        }
