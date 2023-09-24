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

    fn apply(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::empty(self.period).nz(Some(1.0)).into(),
            Series::empty(self.period).nz(Some(1.0)).into(),
        )
    }
}
