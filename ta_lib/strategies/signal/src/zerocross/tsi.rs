use base::prelude::*;
use core::prelude::*;
use momentum::tsi;
use timeseries::prelude::*;

pub struct TsiZeroCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
}

impl TsiZeroCrossSignal {
    pub fn new(
        source_type: SourceType,
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
    ) -> Self {
        Self {
            source_type,
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for TsiZeroCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tsi = tsi(
            &data.source(self.source_type),
            self.smooth_type,
            self.slow_period,
            self.fast_period,
        );

        (tsi.cross_over(&ZERO), tsi.cross_under(&ZERO))
    }
}
