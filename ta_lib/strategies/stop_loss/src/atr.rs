use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct AtrStopLoss {
    period: usize,
    factor: f32,
}

impl AtrStopLoss {
    pub fn new(period: f32, factor: f32) -> Self {
        Self {
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
        let atr_multi = data.atr(self.period) * self.factor;

        (data.low() - &atr_multi, data.high() + &atr_multi)
    }
}
