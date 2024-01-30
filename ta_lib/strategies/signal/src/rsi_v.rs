use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_UPPER_BARRIER: f32 = 80.0;
const RSI_LOWER_BARRIER: f32 = 20.0;

pub struct RSIVSignal {
    rsi_period: usize,
    threshold: f32,
}

impl RSIVSignal {
    pub fn new(rsi_period: f32, threshold: f32) -> Self {
        Self {
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RSIVSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.rsi_period);
        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;

        (
            rsi.sgt(&lower_barrier)
                & rsi.shift(1).slt(&RSI_LOWER_BARRIER)
                & rsi.shift(2).sgt(&RSI_LOWER_BARRIER),
            rsi.slt(&upper_barrier)
                & rsi.shift(1).sgt(&RSI_UPPER_BARRIER)
                & rsi.shift(2).slt(&RSI_UPPER_BARRIER),
        )
    }
}
