use base::{OHLCVSeries, Price, StopLoss};
use core::Series;

pub struct ATRStopLoss {
    pub period: usize,
    pub multi: f32,
}

impl ATRStopLoss {
    pub fn new(period: f32, multi: f32) -> Self {
        Self {
            period: period as usize,
            multi,
        }
    }
}

impl StopLoss for ATRStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr_multi = data.atr(self.period) * self.multi;

        (&data.low - &atr_multi, &data.high + &atr_multi)
    }
}
