use base::prelude::*;
use core::prelude::*;

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
            Series::one(self.period).into(),
            Series::one(self.period).into(),
        )
    }
}
