use base::{OHLCVSeries, Signal};
use core::prelude::*;
use momentum::cc;

const ZERO_LINE: f32 = 0.0;

pub struct CCFlipSignal {
    short_period: usize,
    long_period: usize,
    smoothing_period: usize,
}

impl CCFlipSignal {
    pub fn new(short_period: f32, long_period: f32, smoothing_period: f32) -> Self {
        Self {
            short_period: short_period as usize,
            long_period: long_period as usize,
            smoothing_period: smoothing_period as usize,
        }
    }
}

impl Signal for CCFlipSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.short_period, self.long_period);
        std::cmp::max(adj_lookback, self.smoothing_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cc = cc(
            &data.close,
            self.short_period,
            self.long_period,
            self.smoothing_period,
        );

        (cc.cross_over(&ZERO_LINE), cc.cross_under(&ZERO_LINE))
    }
}
