use base::prelude::*;
use core::prelude::*;
use momentum::tsi;

const TSI_ZERO_LINE: f32 = 0.0;

pub struct TSIFlipSignal {
    smooth_type: Smooth,
    long_period: usize,
    short_period: usize,
}

impl TSIFlipSignal {
    pub fn new(smooth_type: Smooth, long_period: f32, short_period: f32) -> Self {
        Self {
            smooth_type,
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
        let tsi = tsi(
            &data.close,
            self.smooth_type,
            self.long_period,
            self.short_period,
        );

        (
            tsi.cross_over(&TSI_ZERO_LINE),
            tsi.cross_under(&TSI_ZERO_LINE),
        )
    }
}
