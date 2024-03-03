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

        let prev_diff = diff.shift(1);
        let back_2_diff = diff.shift(2);

        (
            ao.sgt(&AO_ZERO)
                & diff.sgt(&AO_ZERO)
                & diff.sgt(&prev_diff)
                & prev_diff.slt(&AO_ZERO)
                & back_2_diff.slt(&AO_ZERO)
                & prev_diff.slt(&back_2_diff),
            ao.slt(&AO_ZERO)
                & diff.slt(&AO_ZERO)
                & diff.slt(&prev_diff)
                & prev_diff.sgt(&AO_ZERO)
                & back_2_diff.sgt(&AO_ZERO)
                & prev_diff.slt(&back_2_diff),
        )
    }
}
