use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct SpreadSignal {
    source: SourceType,
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
}

impl SpreadSignal {
    pub fn new(source: SourceType, smooth: Smooth, period_fast: f32, period_slow: f32) -> Self {
        Self {
            source,
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Signal for SpreadSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let spread =
            data.source(self.source)
                .spread(self.smooth, self.period_fast, self.period_slow);

        let prev_spread = spread.shift(1);

        (
            spread.cross_over(&prev_spread),
            spread.cross_under(&prev_spread),
        )
    }
}
