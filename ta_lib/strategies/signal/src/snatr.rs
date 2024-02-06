use base::prelude::*;
use core::prelude::*;
use volatility::snatr;

const SNATR_UPPER_BARRIER: f32 = 0.8;
const SNATR_LOWER_BARRIER: f32 = 0.2;

pub struct SNATRSignal {
    smooth_type: Smooth,
    atr_period: usize,
    atr_smoothing_period: usize,
    threshold: f32,
}

impl SNATRSignal {
    pub fn new(
        smooth_type: Smooth,
        atr_period: f32,
        atr_smoothing_period: f32,
        threshold: f32,
    ) -> Self {
        Self {
            smooth_type,
            atr_period: atr_period as usize,
            atr_smoothing_period: atr_smoothing_period as usize,
            threshold,
        }
    }
}

impl Signal for SNATRSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.atr_smoothing_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let snatr = snatr(
            &data.atr(self.atr_period),
            self.atr_period,
            self.smooth_type,
            self.atr_smoothing_period,
        );
        let upper_barrier = SNATR_UPPER_BARRIER - self.threshold;
        let lower_barrier = SNATR_LOWER_BARRIER + self.threshold;

        (
            snatr.cross_under(&upper_barrier),
            snatr.cross_over(&lower_barrier),
        )
    }
}
