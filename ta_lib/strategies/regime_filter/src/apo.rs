use base::{OHLCVSeries, Regime};
use core::Series;
use momentum::apo;

const APO_FILTER: f32 = 0.0;

pub struct APOFilter {
    fast_period: usize,
    slow_period: usize,
}

impl APOFilter {
    pub fn new(fast_period: f32, slow_period: f32) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Regime for APOFilter {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let apo_value = apo(&data.close, self.fast_period, self.slow_period);

        (apo_value.sgt(APO_FILTER), apo_value.slt(APO_FILTER))
    }
}
