use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct DumbConfirm {
    period: usize,
}

impl DumbConfirm {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Confirm for DumbConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let len = data.len();

        (Series::one(len).into(), Series::one(len).into())
    }
}
