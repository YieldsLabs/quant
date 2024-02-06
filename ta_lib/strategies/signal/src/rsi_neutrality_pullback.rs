use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_NEUTRALITY: f32 = 50.0;

pub struct RSINeutralityPullbackSignal {
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
}

impl RSINeutralityPullbackSignal {
    pub fn new(smooth_type: Smooth, rsi_period: f32, threshold: f32) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RSINeutralityPullbackSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.smooth_type, self.rsi_period);
        let upper_neutrality = RSI_NEUTRALITY + self.threshold;
        let lower_neutrality = RSI_NEUTRALITY - self.threshold;

        (
            rsi.shift(1).sgt(&RSI_NEUTRALITY)
                & rsi.shift(1).slt(&lower_neutrality)
                & rsi.shift(1).slt(&rsi.shift(2))
                & rsi.shift(2).sgt(&RSI_NEUTRALITY)
                & rsi.shift(3).slt(&RSI_NEUTRALITY),
            rsi.shift(1).slt(&RSI_NEUTRALITY)
                & rsi.shift(1).sgt(&upper_neutrality)
                & rsi.shift(1).sgt(&rsi.shift(2))
                & rsi.shift(2).slt(&RSI_NEUTRALITY)
                & rsi.shift(3).sgt(&RSI_NEUTRALITY),
        )
    }
}
