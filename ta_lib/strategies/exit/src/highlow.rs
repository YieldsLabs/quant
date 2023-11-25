use base::{Exit, OHLCVSeries};
use core::Series;

pub struct HighLowExit {
    period: usize,
}

impl HighLowExit {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Exit for HighLowExit {
    fn lookback(&self) -> usize {
        self.period
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            data.close.gt(&data.high.shift(self.period)),
            data.close.lt(&data.low.shift(self.period)),
        )
    }
}
