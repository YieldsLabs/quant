use base::prelude::*;
use core::prelude::*;

pub struct BraidPulse {
    period_one: usize,
    period_two: usize,
    period_three: usize,
    strength: f32,
    atr_period: usize,
}

impl BraidPulse {
    pub fn new(
        period_one: f32,
        period_two: f32,
        period_three: f32,
        strength: f32,
        atr_period: f32,
    ) -> Self {
        Self {
            period_one: period_one as usize,
            period_two: period_two as usize,
            period_three: period_three as usize,
            strength,
            atr_period: atr_period as usize,
        }
    }
}

impl Pulse for BraidPulse {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.period_one, self.period_two);
        std::cmp::max(adj_lookback, self.period_three)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_one = data.close.ema(self.period_one);
        let ma_two = data.open.ema(self.period_two);
        let ma_three = data.close.ema(self.period_three);
        let filter = data.atr(self.atr_period) * self.strength / 100.0;

        let max = ma_one.max(&ma_two).max(&ma_three);
        let min = ma_one.min(&ma_two).min(&ma_three);

        let diff = max - min;

        let len = data.close.len();
        
        let regime = iff!(
            ma_one.sgt(&ma_two),
            Series::one(len),
            iff!(
                ma_one.slt(&ma_two),
                Series::fill(-1.0, len),
                Series::zero(len)
            )
        );

        let prev_regime = regime.shift(1);

        (
            prev_regime.sne(&1.0) & regime.seq(&1.0) & diff.sgt(&filter),
            prev_regime.sne(&-1.0) & regime.seq(&-1.0) & diff.sgt(&filter),
        )
    }
}
