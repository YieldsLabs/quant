use base::prelude::*;
use core::prelude::*;
use momentum::trix;

const TRIX_ZERO: f32 = 0.0;

pub struct TRIXFlipSignal {
    period: usize,
}

impl TRIXFlipSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for TRIXFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(&data.close, self.period);

        (trix.cross_over(&TRIX_ZERO), trix.cross_under(&TRIX_ZERO))
    }
}
