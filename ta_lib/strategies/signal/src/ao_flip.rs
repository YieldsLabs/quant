use base::prelude::*;
use core::prelude::*;
use momentum::ao;

const AO_ZERO: f32 = 0.0;

pub struct AOFlipSignal {
    fast_period: usize,
    slow_period: usize,
}

impl AOFlipSignal {
    pub fn new(fast_period: f32, slow_period: f32) -> Self {
        Self {
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
        }
    }
}

impl Signal for AOFlipSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.fast_period, self.slow_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let ao = ao(&data.hl2(), self.fast_period, self.slow_period);
        let prev_ao = ao.shift(2);

        (
            ao.cross_over(&AO_ZERO) & prev_ao.slt(&AO_ZERO),
            ao.cross_under(&AO_ZERO) & prev_ao.sgt(&AO_ZERO),
        )
    }
}
