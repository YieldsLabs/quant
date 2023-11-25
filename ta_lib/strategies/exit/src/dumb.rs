use base::{Exit, OHLCVSeries};
use core::Series;

pub struct DumbExit {}

impl Exit for DumbExit {
    fn lookback(&self) -> usize {
        0
    }

    fn evaluate(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
