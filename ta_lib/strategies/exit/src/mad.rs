use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct MadExit {
    source: SourceType,
    period_fast: usize,
    period_slow: usize,
}

impl MadExit {
    pub fn new(source: SourceType, period_fast: f32, period_slow: f32) -> Self {
        Self {
            source,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Exit for MadExit {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let mad =
            data.source(self.source)
                .spread_pct(Smooth::SMA, self.period_fast, self.period_slow);

        (mad.cross_under(&ZERO), mad.cross_over(&ZERO))
    }
}
