use base::prelude::*;
use core::prelude::*;
use momentum::bop;

const BOP_ZERO: f32 = 0.0;

pub struct BOPFlipSignal {
    smooth_type: Smooth,
    smoothing_period: usize,
}

impl BOPFlipSignal {
    pub fn new(smooth_type: Smooth, smoothing_period: f32) -> Self {
        Self {
            smooth_type,
            smoothing_period: smoothing_period as usize,
        }
    }
}

impl Signal for BOPFlipSignal {
    fn lookback(&self) -> usize {
        self.smoothing_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let bop = bop(
            &data.open,
            &data.high,
            &data.low,
            &data.close,
            self.smooth_type,
            self.smoothing_period,
        );

        (bop.cross_over(&BOP_ZERO), bop.cross_under(&BOP_ZERO))
    }
}
