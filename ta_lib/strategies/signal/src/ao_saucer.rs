use base::prelude::*;
use core::prelude::*;
use momentum::ao;

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
        let ao = ao(&data.hl2(), self.short_period, self.long_period);
        let diff = &ao - ao.shift(1);

        (
            ao.sgt(&AO_ZERO)
                & diff.sgt(&AO_ZERO)
                & diff.shift(1).slt(&AO_ZERO)
                & diff.shift(2).slt(&AO_ZERO)
                & diff.shift(1).slt(&diff.shift(2)),
            ao.slt(&AO_ZERO)
                & diff.slt(&AO_ZERO)
                & diff.shift(1).sgt(&AO_ZERO)
                & diff.shift(2).sgt(&AO_ZERO)
                & diff.shift(1).slt(&diff.shift(2)),
        )
    }
}
