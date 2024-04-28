use base::prelude::*;
use core::prelude::*;
use momentum::trix;

pub struct TrixZeroCrossSignal {
    smooth_type: Smooth,
    period: usize,
}

impl TrixZeroCrossSignal {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for TrixZeroCrossSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(data.close(), self.smooth_type, self.period);

        (trix.cross_over(&ZERO_LINE), trix.cross_under(&ZERO_LINE))
    }
}
