use base::prelude::*;
use core::prelude::*;
use trend::vi;

pub struct VICrossSignal {
    atr_period: usize,
    period: usize,
}

impl VICrossSignal {
    pub fn new(atr_period: f32, period: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            period: period as usize,
        }
    }
}

impl Signal for VICrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (vip, vim) = vi(
            &data.high,
            &data.low,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.period,
        );

        (vip.cross_over(&vim), vim.cross_over(&vip))
    }
}
