use base::{OHLCVSeries, Pulse};
use core::Series;

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

    fn assess(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            Series::fill(1.0, self.period).into(),
            Series::fill(1.0, self.period).into(),
        )
    }
}
