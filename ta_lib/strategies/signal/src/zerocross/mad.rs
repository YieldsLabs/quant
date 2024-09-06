use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct MadZeroCrossSignal {
    source: SourceType,
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
}

impl MadZeroCrossSignal {
    pub fn new(source: SourceType, smooth: Smooth, period_fast: f32, period_slow: f32) -> Self {
        Self {
            source,
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Signal for MadZeroCrossSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let mad =
            data.source(self.source)
                .spread_pct(self.smooth, self.period_fast, self.period_slow);

        (mad.cross_over(&ZERO), mad.cross_under(&ZERO))
    }
}
