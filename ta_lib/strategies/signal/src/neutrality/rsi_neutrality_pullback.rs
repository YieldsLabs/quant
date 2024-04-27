use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

pub struct RsiNeutralityPullbackSignal {
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
}

impl RsiNeutralityPullbackSignal {
    pub fn new(smooth_type: Smooth, rsi_period: f32, threshold: f32) -> Self {
        Self {
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RsiNeutralityPullbackSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close(), self.smooth_type, self.rsi_period);
        let upper_neutrality = NEUTRALITY_LINE + self.threshold;
        let lower_neutrality = NEUTRALITY_LINE - self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            prev_rsi.sgt(&NEUTRALITY_LINE)
                & prev_rsi.slt(&lower_neutrality)
                & prev_rsi.slt(&back_2_rsi)
                & back_2_rsi.sgt(&NEUTRALITY_LINE)
                & back_3_rsi.slt(&NEUTRALITY_LINE),
            prev_rsi.slt(&NEUTRALITY_LINE)
                & prev_rsi.sgt(&upper_neutrality)
                & prev_rsi.sgt(&back_2_rsi)
                & back_2_rsi.slt(&NEUTRALITY_LINE)
                & back_3_rsi.sgt(&NEUTRALITY_LINE),
        )
    }
}
