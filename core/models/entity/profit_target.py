from functools import cached_property

import numpy as np

from core.models.side import SignalSide

from ._base import Entity


@Entity
class ProfitTarget:
    _side: SignalSide
    entry: float
    _volatility: float
    _noise_sigma: float = 0.001

    @cached_property
    def targets(self):
        ratios = [
            0.236,
            0.272,
            0.382,
            0.414,
            0.618,
            0.786,
            0.886,
            1.0,
            1.118,
            1.236,
            1.382,
            1.618,
            1.786,
            1.886,
            2.0,
            2.236,
            2.382,
            2.618,
            2.786,
            3.0,
            3.236,
            3.382,
            3.618,
            4.0,
            4.236,
            4.382,
            4.618,
            5.0,
            5.236,
            5.382,
            5.618,
            6.0,
            6.236,
            6.382,
            6.618,
            7.0,
            7.236,
            7.382,
            7.618,
            8.0,
            8.236,
            8.382,
            8.618,
            9.0,
            9.236,
            9.382,
            9.618,
            10.0,
            10.236,
            10.382,
            10.618,
            11.0,
            11.236,
            11.382,
            11.618,
            12.0,
            12.236,
            12.382,
            12.618,
            13.0,
            13.236,
            13.382,
            13.618,
            14.0,
            14.236,
            14.382,
            14.618,
            15.0,
            15.236,
            15.382,
            15.618,
            16.0,
            16.236,
            16.382,
            16.618,
            17.0,
            17.236,
            17.382,
            17.618,
            18.0,
        ]

        levels = sorted(
            {
                self._pt(ratios[i], ratios[j])
                for i in range(len(ratios))
                for j in range(i, len(ratios))
            }
        )

        reverse = self._context_factor() == -1
        return levels if not reverse else levels[::-1]

    @cached_property
    def last(self):
        return self.targets[-1]

    def _context_factor(self):
        return 1.0 if self._side == SignalSide.BUY else -1.0

    def _pt(self, min_scale: float, max_scale: float) -> float:
        scale = np.random.uniform(min_scale, max_scale)
        noise = np.random.lognormal(mean=0, sigma=self._noise_sigma) - 1
        target_price = self.entry * (
            1 + self._volatility * self._context_factor() * scale + noise
        )

        return (
            max(target_price, self.entry)
            if self._context_factor() == 1
            else min(target_price, self.entry)
        )
