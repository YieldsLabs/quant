use base::{Filter, OHLCVSeries};
use core::Series;

pub struct DumbFilter {
    period: usize,
}

impl DumbFilter {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Filter for DumbFilter {
    fn lookback(&self) -> usize {
        self.period
    }

    fn confirm(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::fill(1.0, self.period).into(),
            Series::fill(1.0, self.period).into(),
        )
    }
}
