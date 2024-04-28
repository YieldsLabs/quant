use base::prelude::*;
use core::prelude::*;

pub struct DumbPulse {
    period: usize,
}

impl DumbPulse {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl Pulse for DumbPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let len = data.len();

        (Series::one(len).into(), Series::one(len).into())
    }
}
