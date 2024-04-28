use base::prelude::*;
use core::prelude::*;
use volume::vo;

pub struct VoPulse {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
}

impl VoPulse {
    pub fn new(smooth_type: Smooth, fast_period: f32, slow_period: f32) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Pulse for VoPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vo = vo(
            data.volume(),
            self.smooth_type,
            self.fast_period,
            self.slow_period,
        );

        (vo.sgt(&ZERO_LINE), vo.sgt(&ZERO_LINE))
    }
}
