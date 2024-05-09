use base::prelude::*;
use core::prelude::*;
use momentum::ao;
use timeseries::prelude::*;

pub struct AoZeroCrossSignal {
    source_type: SourceType,
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
}

impl AoZeroCrossSignal {
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

impl Signal for AoZeroCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = ao(
            &data.source(self.source_type),
            self.smooth_type,
            self.fast_period,
            self.slow_period,
        );

        (ao.cross_over(&ZERO_LINE), ao.cross_under(&ZERO_LINE))
    }
}
