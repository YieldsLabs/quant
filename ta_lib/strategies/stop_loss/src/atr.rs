use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct AtrStopLoss {
    smooth: Smooth,
    period: usize,
    factor: f32,
}

impl AtrStopLoss {
    pub fn new(smooth: Smooth, period: f32, factor: f32) -> Self {
        Self {
            smooth,
            period: period as usize,
            factor,
        }
    }
}

impl StopLoss for AtrStopLoss {
    fn lookback(&self) -> usize {
        self.period
    }

    fn find(&self, data: &OHLCVSeries) -> (Price, Price) {
        let atr_multi = data.atr(self.smooth, self.period) * self.factor;

        (data.low() - &atr_multi, data.high() + &atr_multi)
    }
}
