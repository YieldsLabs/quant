use base::{OHLCVSeries, Signal};
use core::prelude::*;
use momentum::tsi;

const TSI_ZERO: f32 = 0.0;

pub struct TSIFlipSignal {
    long_period: usize,
    short_period: usize,
}

impl TSIFlipSignal {
    pub fn new(long_period: f32, short_period: f32) -> Self {
        Self {
            long_period: long_period as usize,
            short_period: short_period as usize,
        }
    }
}

impl Signal for TSIFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tsi = tsi(&data.close, self.long_period, self.short_period);

        (tsi.cross_over(&TSI_ZERO), tsi.cross_under(&TSI_ZERO))
    }
}
