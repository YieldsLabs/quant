use base::prelude::*;
use core::prelude::*;
use momentum::bop;
use timeseries::prelude::*;

pub struct BopZeroCrossSignal {
    smooth_type: Smooth,
    smooth_period: usize,
}

impl BopZeroCrossSignal {
    pub fn new(smooth_type: Smooth, smooth_period: f32) -> Self {
        Self {
            smooth_type,
            smooth_period: smooth_period as usize,
        }
    }
}

impl Signal for BopZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.smooth_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let bop = bop(
            data.open(),
            data.high(),
            data.low(),
            data.close(),
            self.smooth_type,
            self.smooth_period,
        );

        (bop.cross_over(&ZERO_LINE), bop.cross_under(&ZERO_LINE))
    }
}
