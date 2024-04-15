use base::prelude::*;
use core::prelude::*;
use trend::vi;

pub struct ViConfirm {
    atr_period: usize,
    period: usize,
}

impl ViConfirm {
    pub fn new(atr_period: f32, period: f32) -> Self {
        Self {
            atr_period: atr_period as usize,
            period: period as usize,
        }
    }
}

impl Confirm for ViConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.period)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (vip, vim) = vi(
            &data.high,
            &data.low,
            &data.atr(self.atr_period, Smooth::SMMA),
            self.period,
        );

        (vip.sgt(&vim), vip.slt(&vim))
    }
}
