use base::prelude::*;
use core::prelude::*;
use momentum::rsi;

pub struct RsiSignalLineSignal {
    smooth_type: Smooth,
    rsi_period: usize,
    smooth_signal: Smooth,
    smooth_period: usize,
    threshold: f32,
}

impl RsiSignalLineSignal {
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

impl Signal for RsiSignalLineSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.rsi_period, self.smooth_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let rsi = rsi(&data.close(), self.smooth_type, self.rsi_period);
        let rsi_ma = rsi.smooth(self.smooth_signal, self.smooth_period);
        let upper_neutrality = NEUTRALITY_LINE + self.threshold;
        let lower_neutrality = NEUTRALITY_LINE - self.threshold;

        let prev_rsi = rsi.shift(1);
        let back_2_rsi = rsi.shift(2);
        let back_3_rsi = rsi.shift(3);

        let prev_rsi_ma = rsi_ma.shift(1);
        let back_3_rsi_ma = rsi_ma.shift(3);

        (
            rsi.sgt(&rsi_ma)
                & rsi.slt(&upper_neutrality)
                & prev_rsi.seq(&prev_rsi_ma)
                & back_2_rsi.sgt(&prev_rsi)
                & back_3_rsi.slt(&back_3_rsi_ma),
            rsi.slt(&rsi_ma)
                & rsi.sgt(&lower_neutrality)
                & prev_rsi.seq(&prev_rsi_ma)
                & back_2_rsi.slt(&prev_rsi)
                & back_3_rsi.sgt(&back_3_rsi_ma),
        )
    }
}
