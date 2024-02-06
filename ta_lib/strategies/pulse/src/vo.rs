use base::prelude::*;
use core::prelude::*;
use volume::vo;

const VO_ZERO_LINE: f32 = 0.0;

pub struct VoPulse {
    smooth_type: Smooth,
    short_period: usize,
    long_period: usize,
}

impl VoPulse {
    pub fn new(smooth_type: Smooth, short_period: f32, long_period: f32) -> Self {
        Self {
            smooth_type,
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Pulse for VoPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let vo = vo(
            &data.volume,
            self.smooth_type,
            self.short_period,
            self.long_period,
        );

        (vo.sgt(&VO_ZERO_LINE), vo.sgt(&VO_ZERO_LINE))
    }
}
