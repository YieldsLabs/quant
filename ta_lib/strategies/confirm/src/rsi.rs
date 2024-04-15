use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_UPPER_BARRIER: f32 = 75.;
const RSI_LOWER_BARRIER: f32 = 35.;

pub struct RsiConfirm {
    smooth_type: Smooth,
    rsi_period: usize,
    smooth_signal: Smooth,
    smooth_period: usize,
    threshold: f32,
}

impl RsiConfirm {
    pub fn new(
        smooth_type: Smooth,
        rsi_period: f32,
        smooth_signal: Smooth,
        smooth_period: f32,
        threshold: f32,
    ) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            smooth_signal,
            smooth_period: smooth_period as usize,
            threshold,
        }
    }
}

impl Confirm for RsiConfirm {
    fn lookback(&self) -> usize {
        std::cmp::max(self.rsi_period, self.smooth_period)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.smooth_type, self.rsi_period);
        let signal = rsi.smooth(self.smooth_signal, self.smooth_period);
        let upper_barrier = RSI_UPPER_BARRIER + self.threshold;
        let lower_barrier = RSI_LOWER_BARRIER - self.threshold;

        (
            rsi.slt(&upper_barrier) & rsi.sgt(&signal),
            rsi.sgt(&lower_barrier) & rsi.slt(&signal),
        )
    }
}
