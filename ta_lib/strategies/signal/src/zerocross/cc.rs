use base::prelude::*;
use core::prelude::*;
use momentum::cc;
use timeseries::prelude::*;

pub struct CcZeroCrossSignal {
    source_type: SourceType,
    fast_period: usize,
    slow_period: usize,
    smooth_type: Smooth,
    smooth_period: usize,
}

impl CcZeroCrossSignal {
    pub fn new(
        source_type: SourceType,
        fast_period: f32,
        slow_period: f32,
        smooth_type: Smooth,
        smooth_period: f32,
    ) -> Self {
        Self {
            source_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            smooth_type,
            smooth_period: smooth_period as usize,
        }
    }
}

impl Signal for CcZeroCrossSignal {
    fn lookback(&self) -> usize {
        let adj_lookback = std::cmp::max(self.fast_period, self.slow_period);
        std::cmp::max(adj_lookback, self.smooth_period)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let cc = cc(
            &data.source(self.source_type),
            self.fast_period,
            self.slow_period,
            self.smooth_type,
            self.smooth_period,
        );

        (cc.cross_over(&ZERO_LINE), cc.cross_under(&ZERO_LINE))
    }
}
