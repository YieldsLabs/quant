use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_UPPER_BARRIER: f32 = 65.0;
const RSI_LOWER_BARRIER: f32 = 35.0;

pub struct RSIConfirm {
    rsi_period: usize,
    threshold: f32,
}

impl RSIConfirm {
    pub fn new(rsi_period: f32, threshold: f32) -> Self {
        Self {
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Confirm for RSIConfirm {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.rsi_period);
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        (rsi.sgt(&upper_barrier), rsi.slt(&lower_barrier))
    }
}
