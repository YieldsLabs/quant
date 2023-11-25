use base::{OHLCVSeries, Pulse};
use core::Series;
use volume::vo;

const VO_THRESHOLD: f32 = 0.0;

pub struct OSCPulse {
    short_period: usize,
    long_period: usize,
}

impl OSCPulse {
    pub fn new(short_period: f32, long_period: f32) -> Self {
        Self {
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Pulse for OSCPulse {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (
            vo(&data.volume, self.short_period, self.long_period).sgt(VO_THRESHOLD),
            vo(&data.volume, self.short_period, self.long_period).sgt(VO_THRESHOLD),
        )
    }
}
