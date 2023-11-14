use base::{OHLCVSeries, Regime};
use core::Series;

const LOOKBACK: usize = 21;

pub struct FibFilter {}

impl FibFilter {
    pub fn new() -> Self {
        Self {}
    }
}

impl Regime for FibFilter {
    fn lookback(&self) -> usize {
        LOOKBACK
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            data.high.gt(&data.low.shift(2))
                & data.high.gt(&data.low.shift(3))
                & data.high.gt(&data.low.shift(5))
                & data.high.gt(&data.low.shift(8))
                & data.high.gt(&data.low.shift(13)),
            data.low.lt(&data.high.shift(2))
                & data.low.lt(&data.high.shift(3))
                & data.low.lt(&data.high.shift(5))
                & data.low.lt(&data.high.shift(8))
                & data.low.lt(&data.high.shift(13)),
        )
    }
}
