use base::{OHLCVSeries, Volume};
use core::Series;

pub struct DumbVolume {
    period: usize,
}

impl DumbVolume {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Volume for DumbVolume {
    fn lookback(&self) -> usize {
        self.period
    }

    fn apply(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::fill(1.0, self.period).into(),
            Series::fill(1.0, self.period).into(),
        )
    }
}
