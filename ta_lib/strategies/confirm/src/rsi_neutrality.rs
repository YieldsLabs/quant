use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

const RSI_UPPER_BARRIER: f32 = 75.0;
const RSI_LOWER_BARRIER: f32 = 25.0;

pub struct RsiNeutralityConfirm {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    threshold: f32,
}

impl RsiNeutralityConfirm {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32, threshold: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            threshold,
        }
    }
}

impl Confirm for RsiNeutralityConfirm {
    fn lookback(&self) -> usize {
        self.period
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
        );

        let lower_barrier = RSI_LOWER_BARRIER + self.threshold;
        let upper_barrier = RSI_UPPER_BARRIER - self.threshold;
        let lower_neutrality = NEUTRALITY_LINE - self.threshold;
        let upper_neutrality = NEUTRALITY_LINE + self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            rsi.sgt(&NEUTRALITY_LINE)
                & rsi.slt(&upper_barrier)
                & prev_rsi.sgt(&lower_neutrality)
                & back_2_rsi.sgt(&lower_neutrality)
                & back_3_rsi.sgt(&lower_neutrality),
            rsi.slt(&NEUTRALITY_LINE)
                & rsi.sgt(&lower_barrier)
                & prev_rsi.slt(&upper_neutrality)
                & back_2_rsi.slt(&upper_neutrality)
                & back_3_rsi.slt(&upper_neutrality),
        )
    }
}
