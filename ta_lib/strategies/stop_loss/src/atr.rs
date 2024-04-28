use base::prelude::*;
use core::prelude::*;

pub struct AtrStopLoss {
    smooth_type: Smooth,
    period: usize,
    factor: f32,
}

impl AtrStopLoss {
    pub fn new(smooth_type: Smooth, period: f32, factor: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            factor,
        }
    }
}

impl StopLoss for AtrStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
        let atr_multi = data.atr(self.period, self.smooth_type) * self.factor;

        (data.low() - &atr_multi, data.high() + &atr_multi)
    }
}
