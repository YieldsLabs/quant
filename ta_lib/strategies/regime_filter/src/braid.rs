use base::{OHLCVSeries, Price, Regime};
use core::Series;

const PIPS_NUM: f32 = 40.0;

pub struct BraidFilter {
    period_one: usize,
    period_two: usize,
    period_three: usize,
    atr_period: usize,
}

impl BraidFilter {
    pub fn new(period_one: f32, period_two: f32, period_three: f32, atr_period: f32) -> Self {
        Self {
            period_one: period_one as usize,
            period_two: period_two as usize,
            period_three: period_three as usize,
            atr_period: atr_period as usize,
        }
    }
}

impl Regime for BraidFilter {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.period_one, self.period_two);
        std::cmp::max(adj_lookback, self.period_three)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ma_one = data.close.ema(self.period_one);
        let ma_two = data.open.ema(self.period_two);
        let ma_three = data.close.ema(self.period_three);
        let filter = data.atr(self.atr_period) * PIPS_NUM / 100.0;

        let max = ma_one.max(&ma_two).max(&ma_three);
        let min = ma_one.min(&ma_two).min(&ma_three);

        let diff = max - min;

        (
            ma_one.gt(&ma_two) & diff.gt(&filter),
            ma_two.gt(&ma_one) & diff.gt(&filter),
        )
    }
}
