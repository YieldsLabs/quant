use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

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

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            data.low().seq(&data.low().shift(1)),
            data.high().seq(&data.high().shift(1)),
        )
    }
}
