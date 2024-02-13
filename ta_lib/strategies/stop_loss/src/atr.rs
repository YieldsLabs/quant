use base::prelude::*;
use core::prelude::*;

pub struct ATRStopLoss {
    pub period: usize,
    pub factor: f32,
}

impl ATRStopLoss {
    pub fn new(period: f32, factor: f32) -> Self {
        Self {
            period: period as usize,
            factor,
        }
    }
}

impl StopLoss for ATRStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr_multi = data.atr(self.period) * self.factor;

        (&data.low - &atr_multi, &data.high + &atr_multi)
    }
}
