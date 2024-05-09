use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

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
            data.close().sgt(&data.high().shift(self.period)),
            data.close().slt(&data.low().shift(self.period)),
        )
    }
}
