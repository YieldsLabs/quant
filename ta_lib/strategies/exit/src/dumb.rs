use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct DumbExit {}

impl Exit for DumbExit {
    fn lookback(&self) -> usize {
        0
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let len = data.len();

        (Series::zero(len).into(), Series::zero(len).into())
    }
}
