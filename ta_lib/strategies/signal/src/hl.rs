use base::{OHLCVSeries, Signal};
use core::Series;

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
            data.low.eq(&data.low.shift(1)),
            data.high.eq(&data.high.shift(1)),
        )
    }
}
