use base::{OHLCVSeries, Pulse};
use core::{Comparator, Series};
use volume::vo;

const VO_THRESHOLD: f32 = 0.0;

pub struct VoPulse {
    short_period: usize,
    long_period: usize,
}

impl VoPulse {
    pub fn new(short_period: f32, long_period: f32) -> Self {
        Self {
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
        let vo = vo(&data.volume, self.short_period, self.long_period);

        (vo.sgt(&VO_THRESHOLD), vo.sgt(&VO_THRESHOLD))
    }
}
