use base::{OHLCVSeries, Regime};
use core::Series;
use momentum::apo;

const APO_FILTER: f32 = 0.0;

pub struct APOFilter {
    short_period: usize,
    long_period: usize,
}

impl APOFilter {
    pub fn new(short_period: f32, long_period: f32) -> Self {
        Self {
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Regime for APOFilter {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let apo = apo(&data.close, self.short_period, self.long_period);

        (apo.sgt(APO_FILTER), apo.slt(APO_FILTER))
    }
}
