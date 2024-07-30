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
            (1.0, 1.236),
            (1.382, 1.618),
            (1.786, 2.0),
            (2.236, 2.618),
            (3.0, 3.236),
            (3.618, 4.0),
            (4.236, 4.618),
            (5.0, 5.236),
            (6.0, 6.618),
            (7.0, 7.786),
            (8.0, 8.618),
            (9.0, 9.786),
            (9.618, 10.236),
            (10.618, 11.236),
            (11.618, 12.236),
            (12.618, 13.236),
            (13.618, 14.236),
            (14.618, 15.236),
            (15.618, 16.236),
            (16.618, 17.236),
        ]

        reverse = True if self.context_factor == -1 else False
        return sorted(
            {self._pt(min_scale, max_scale) for min_scale, max_scale in levels},
            reverse=reverse,
        )

    @cached_property
    def last(self):
        return self.targets[-1]

    def _pt(self, min_scale: float, max_scale: float) -> float:
        scale = np.random.uniform(min_scale, max_scale)
        noise = np.random.normal(0, 0.001)
        target_price = self.entry * (
            1 + self.volatility * self.context_factor * scale + noise
        )

        return (
            max(target_price, self.entry)
            if self.context_factor == 1
            else min(target_price, self.entry)
        )

    def to_dict(self):
        return {
            "targets": self.targets,
        }
