use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct AoZeroCrossSignal {
    source: SourceType,
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
}

impl AoZeroCrossSignal {
    pub fn new(source: SourceType, smooth: Smooth, period_fast: f32, period_slow: f32) -> Self {
        Self {
            source,
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Signal for AoZeroCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = data
            .source(self.source)
            .spread(self.smooth, self.period_fast, self.period_slow);

        (ao.cross_over(&ZERO_LINE), ao.cross_under(&ZERO_LINE))
    }
}
