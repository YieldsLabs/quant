use base::prelude::*;
use core::prelude::*;
use timeseries::prelude::*;

pub struct VoPulse {
    smooth: Smooth,
    period_fast: usize,
    period_slow: usize,
}

impl VoPulse {
    pub fn new(smooth: Smooth, period_fast: f32, period_slow: f32) -> Self {
        Self {
            smooth,
            period_fast: period_fast as usize,
            period_slow: period_slow as usize,
        }
    }
}

impl Pulse for VoPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period_fast, self.period_slow)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vo = data
            .volume()
            .pspread(self.smooth, self.period_fast, self.period_slow);

        (vo.sgt(&ZERO_LINE), vo.sgt(&ZERO_LINE))
    }
}
