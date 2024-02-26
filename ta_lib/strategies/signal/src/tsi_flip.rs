use base::prelude::*;
use core::prelude::*;
use momentum::tsi;

const TSI_ZERO_LINE: f32 = 0.0;

pub struct TSIFlipSignal {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
}

impl TSIFlipSignal {
    pub fn new(smooth_type: Smooth, fast_period: f32, slow_period: f32) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for TSIFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tsi = tsi(
            &data.close,
            self.smooth_type,
            self.slow_period,
            self.fast_period,
        );

        (
            tsi.cross_over(&TSI_ZERO_LINE),
            tsi.cross_under(&TSI_ZERO_LINE),
        )
    }
}
