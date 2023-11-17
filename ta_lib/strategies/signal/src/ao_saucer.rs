use base::{OHLCVSeries, Price, Signal};
use core::Series;
use trend::aosc;

const AO_ZERO: f32 = 0.0;

pub struct AOSaucerSignal {
    short_period: usize,
    long_period: usize,
}

impl AOSaucerSignal {
    pub fn new(short_period: f32, long_period: f32) -> Self {
        Self {
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for AOSaucerSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = aosc(&data.hl2(), self.short_period, self.long_period);
        (
            ao.sgt(AO_ZERO)
                & ao.shift(1).gt(&ao)
                & ao.shift(2).gt(&ao.shift(1))
                & ao.shift(3).gt(&ao.shift(2))
                & ao.shift(4).lt(&ao.shift(3)),
            ao.slt(AO_ZERO)
                & ao.shift(1).lt(&ao)
                & ao.shift(2).lt(&ao.shift(1))
                & ao.shift(3).lt(&ao.shift(2))
                & ao.shift(4).gt(&ao.shift(3)),
        )
    }
}
