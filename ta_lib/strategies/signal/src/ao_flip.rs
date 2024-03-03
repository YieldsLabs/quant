use base::prelude::*;
use core::prelude::*;
use momentum::ao;

const AO_ZERO: f32 = 0.0;

pub struct AOFlipSignal {
    short_period: usize,
    long_period: usize,
}

impl AOFlipSignal {
    pub fn new(short_period: f32, long_period: f32) -> Self {
        Self {
            short_period: short_period as usize,
            long_period: long_period as usize,
        }
    }
}

impl Signal for AOFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.short_period, self.long_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = ao(&data.hl2(), self.short_period, self.long_period);
        let prev_ao = ao.shift(2);

        (
            ao.cross_over(&AO_ZERO) & prev_ao.slt(&AO_ZERO),
            ao.cross_under(&AO_ZERO) & prev_ao.sgt(&AO_ZERO),
        )
    }
}
