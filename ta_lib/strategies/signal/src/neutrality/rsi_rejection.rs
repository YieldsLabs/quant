use base::prelude::*;
use core::prelude::*;
use momentum::rsi;
use timeseries::prelude::*;

pub struct RsiNeutralityRejectionSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    rsi_period: usize,
    threshold: f32,
}

impl RsiNeutralityRejectionSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        rsi_period: f32,
        threshold: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            rsi_period: rsi_period as usize,
            threshold,
        }
    }
}

impl Signal for RsiNeutralityRejectionSignal {
    fn lookback(&self) -> usize {
        self.rsi_period
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.rsi_period,
        );
        let upper_neutrality = NEUTRALITY + self.threshold;
        let lower_neutrality = NEUTRALITY - self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        (
            rsi.sgt(&upper_neutrality)
                & prev_rsi.slt(&NEUTRALITY)
                & back_2_rsi.sgt(&NEUTRALITY)
                & back_3_rsi.sgt(&NEUTRALITY),
            rsi.slt(&lower_neutrality)
                & prev_rsi.sgt(&NEUTRALITY)
                & back_2_rsi.slt(&NEUTRALITY)
                & back_3_rsi.slt(&NEUTRALITY),
        )
    }
}
