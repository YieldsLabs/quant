use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct AoSaucerSignal {
    source: SourceType,
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
}

impl AoSaucerSignal {
    pub fn new(source: SourceType, smooth: Smooth, period_fast: f32, period_slow: f32) -> Self {
        Self {
            source,
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Signal for AoSaucerSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = data
            .source(self.source)
            .spread(self.smooth, self.period_fast, self.period_slow);
        let diff = &ao - ao.shift(1);

        let prev_diff = diff.shift(1);
        let back_2_diff = diff.shift(2);

        (
            ao.sgt(&ZERO)
                & diff.sgt(&ZERO)
                & diff.sgt(&prev_diff)
                & prev_diff.slt(&ZERO)
                & back_2_diff.slt(&ZERO)
                & prev_diff.slt(&back_2_diff),
            ao.slt(&ZERO)
                & diff.slt(&ZERO)
                & diff.slt(&prev_diff)
                & prev_diff.sgt(&ZERO)
                & back_2_diff.sgt(&ZERO)
                & prev_diff.slt(&back_2_diff),
        )
    }
}
