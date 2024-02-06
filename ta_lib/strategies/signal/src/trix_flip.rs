use base::prelude::*;
use core::prelude::*;
use momentum::trix;

const TRIX_ZERO: f32 = 0.0;

pub struct TRIXFlipSignal {
    smooth_type: Smooth,
    period: usize,
}

impl TRIXFlipSignal {
    pub fn new(smooth_type: Smooth, period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
        }
    }
}

impl Signal for TRIXFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(&data.close, self.smooth_type, self.period);

        (trix.cross_over(&TRIX_ZERO), trix.cross_under(&TRIX_ZERO))
    }
}
