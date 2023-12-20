use base::{OHLCVSeries, Signal};
use core::prelude::*;
use momentum::cfo;

const CFO_ZERO: f32 = 0.0;

pub struct CFOFlipSignal {
    period: usize,
}

impl CFOFlipSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for CFOFlipSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cfo = cfo(&data.close, self.period);

        (cfo.cross_over(&CFO_ZERO), cfo.cross_under(&CFO_ZERO))
    }
}
