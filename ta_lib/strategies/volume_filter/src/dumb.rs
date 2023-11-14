use base::{OHLCVSeries, Volume};
use core::Series;

pub struct DumbVolume {}

impl Volume for DumbVolume {
    fn lookback(&self) -> usize {
        0
    }

    fn apply(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}
