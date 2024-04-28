use base::prelude::*;
use core::prelude::*;

pub struct DumbExit {}

impl Exit for DumbExit {
    fn lookback(&self) -> usize {
        0
    }

    fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let len = data.len();

        (Series::zero(len).into(), Series::zero(len).into())
    }
}
