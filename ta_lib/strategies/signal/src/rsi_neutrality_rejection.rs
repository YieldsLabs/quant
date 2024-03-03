use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

const RSI_NEUTRALITY: f32 = 50.0;

pub struct RSINeutralityRejectionSignal {
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
}

impl RSINeutralityRejectionSignal {
    pub fn new(smooth_type: Smooth, rsi_period: f32, threshold: f32) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RSINeutralityRejectionSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close, self.smooth_type, self.rsi_period);
        let upper_neutrality = RSI_NEUTRALITY + self.threshold;
        let lower_neutrality = RSI_NEUTRALITY - self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            rsi.sgt(&upper_neutrality)
                & prev_rsi.slt(&RSI_NEUTRALITY)
                & back_2_rsi.sgt(&RSI_NEUTRALITY)
                & back_3_rsi.sgt(&RSI_NEUTRALITY),
            rsi.slt(&lower_neutrality)
                & prev_rsi.sgt(&RSI_NEUTRALITY)
                & back_2_rsi.slt(&RSI_NEUTRALITY)
                & back_3_rsi.slt(&RSI_NEUTRALITY),
        )
    }
}
