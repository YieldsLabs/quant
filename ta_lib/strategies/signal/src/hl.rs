use base::{OHLCVSeries, Signal};
use core::prelude::*;

pub struct HighLowSignal {
    period: usize,
}

impl HighLowSignal {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Signal for HighLowSignal {
    fn lookback(&self) -> usize {
        self.period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            data.low.seq(&data.low.shift(1)),
            data.high.seq(&data.high.shift(1)),
        )
    }
}
