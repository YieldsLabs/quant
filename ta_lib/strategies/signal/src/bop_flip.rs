use base::{OHLCVSeries, Signal};
use core::Series;
use momentum::bop;

const BOP_ZERO: f32 = 0.0;

pub struct BOPFlipSignal {
    smoothing_period: usize,
}

impl BOPFlipSignal {
    pub fn new(smoothing_period: f32) -> Self {
        Self {
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
            self.smoothing_period,
        );

        (
            bop.cross_over_line(BOP_ZERO),
            bop.cross_under_line(BOP_ZERO),
        )
    }
}
