use base::prelude::*;
use core::prelude::*;
use volatility::dch;

pub struct DchStopLoss {
    period: usize,
}

impl DchStopLoss {
    pub fn new(period: f32) -> Self {
        Self {
            period: period as usize,
        }
    }
}

impl StopLoss for DchStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let (upper, _, lower) = dch(&data.high, &data.low, self.period);

        (lower, upper)
    }
}
