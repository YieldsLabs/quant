use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;
use volatility::snatr;

const SNATR_UPPER_BARRIER: f32 = 80.;
const SNATR_LOWER_BARRIER: f32 = 20.;

pub struct SnatrReversalSignal {
    smooth_type: Smooth,
    atr_period: usize,
    atr_smooth_period: usize,
    threshold: f32,
}

impl SnatrReversalSignal {
    pub fn new(
        smooth_type: Smooth,
        atr_period: f32,
        atr_smooth_period: f32,
        threshold: f32,
    ) -> Self {
        Self {
            smooth_type,
            atr_period: atr_period as usize,
            atr_smooth_period: atr_smooth_period as usize,
            threshold,
        }
    }
}

impl Signal for SnatrReversalSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.atr_smooth_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let snatr = snatr(
            &data.atr(self.atr_period),
            self.atr_period,
            self.smooth_type,
            self.atr_smooth_period,
        );
        let upper_barrier = SNATR_UPPER_BARRIER - self.threshold;
        let lower_barrier = SNATR_LOWER_BARRIER + self.threshold;

        (
            snatr.cross_under(&upper_barrier),
            snatr.cross_over(&lower_barrier),
        )
    }
}
